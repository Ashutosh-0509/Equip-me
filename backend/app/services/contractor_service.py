import random
from datetime import datetime, date
from typing import Optional, Any
from backend.app.database.db import db
from backend.app.schemas.domain_schemas import BookingCreateRequest

class ContractorService:
    @staticmethod
    def get_catalogue(category: Optional[str] = None, search: Optional[str] = None) -> list[dict[str, Any]]:
        with db.lock:
            items = list(db.catalogue)
            if category and category.lower() != "all":
                items = [i for i in items if category.lower() in i["category"].lower()]
            if search:
                q = search.lower().strip()
                items = [i for i in items if q in i["name"].lower() or q in i["description"].lower()]
            return items

    @staticmethod
    def get_bookings(contractor_id: Optional[str] = None, status: Optional[str] = None) -> list[dict[str, Any]]:
        all_b = db.get_all_bookings()
        if contractor_id:
            all_b = [b for b in all_b if b.get("contractor_id") == contractor_id]
        if status and status.lower() != "all":
            if status.lower() == "active":
                active_statuses = {"pending_provider", "pending_approval", "approved", "assigned", "in_transit", "arrived", "working", "awaiting_end"}
                all_b = [b for b in all_b if b.get("status") in active_statuses]
            elif status.lower() == "completed":
                all_b = [b for b in all_b if b.get("status") == "completed"]
            elif status.lower() == "issues":
                all_b = [b for b in all_b if b.get("status") in ("problem", "rejected", "cancelled")]
            else:
                all_b = [b for b in all_b if b.get("status") == status]
        return all_b

    @staticmethod
    def get_booking(booking_id: str) -> Optional[dict[str, Any]]:
        return db.get_booking_by_id(booking_id)

    @staticmethod
    def create_booking(data: BookingCreateRequest, contractor_id: str = "contractor-1") -> dict[str, Any]:
        with db.lock:
            eq = next((e for e in db.catalogue if e["id"] == data.equipment_id), None)
            if not eq:
                raise ValueError(f"Equipment with ID {data.equipment_id} not found.")

            next_num = 8840 + len(db.bookings)
            booking_id = f"BMC-{next_num}"
            hours = data.hours if data.hours else 8
            line_amount = eq["rate"] * data.quantity * hours
            
            line = {
                "equipment_id": eq["id"],
                "name": eq["name"],
                "quantity": data.quantity,
                "rate": eq["rate"],
                "hours": hours,
                "amount": line_amount,
            }

            start_pin = f"{random.randint(1000, 9999)}"
            end_pin = f"{random.randint(1000, 9999)}"
            now_iso = datetime.now().isoformat()

            new_booking = {
                "id": booking_id,
                "contractor_id": contractor_id,
                "provider_id": eq.get("provider_id", "provider-1"),
                "status": "pending_provider",
                "date": data.date,
                "shift": data.shift,
                "hours": hours,
                "address": data.address,
                "ward": data.ward,
                "latitude": data.latitude or "19.0830",
                "longitude": data.longitude or "72.8370",
                "work_order": data.work_order,
                "lines": [line],
                "total": line_amount,
                "assignments": [],
                "requested_lines": [line],
                "requested_total": line_amount,
                "provider_reviewed": False,
                "start_pin": start_pin,
                "end_pin": end_pin,
                "started_at": "",
                "ended_at": "",
                "reason": "",
                "safety_confirmed": data.safety_confirmed,
            }

            db.bookings.insert(0, new_booking)

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": contractor_id,
                "action": "created",
                "timestamp": now_iso,
                "note": f"Requisition created for {data.quantity}x {eq['name']}",
            })

            return db.enrich_booking(new_booking)

    @staticmethod
    def cancel_booking(booking_id: str, reason: str, actor_id: str = "contractor-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")
            if booking["status"] in ("completed", "working", "awaiting_end"):
                raise ValueError(f"Cannot cancel booking in '{booking['status']}' state")

            booking["status"] = "cancelled"
            booking["reason"] = reason

            # release assigned vehicles/operators
            for a in booking.get("assignments", []):
                v = next((veh for veh in db.vehicles if veh["id"] == a.get("vehicle_id")), None)
                if v:
                    v["status"] = "available"
                op = next((o for o in db.operators if o["id"] == a.get("operator_id")), None)
                if op:
                    op["status"] = "available"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": actor_id,
                "action": "cancelled",
                "timestamp": datetime.now().isoformat(),
                "note": f"Cancelled by contractor: {reason}",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def report_dispute(booking_id: str, category: str, description: str, contractor_id: str = "contractor-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "problem"
            booking["reason"] = description

            dispute = {
                "id": f"dispute-{len(db.disputes) + 1}",
                "booking_id": booking_id,
                "contractor_id": contractor_id,
                "category": category,
                "description": description,
                "status": "open",
                "resolution": "",
                "created_at": datetime.now().isoformat(),
            }
            db.disputes.append(dispute)

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": contractor_id,
                "action": "dispute_reported",
                "timestamp": datetime.now().isoformat(),
                "note": f"Dispute filed ({category}): {description}",
            })

            return dispute
