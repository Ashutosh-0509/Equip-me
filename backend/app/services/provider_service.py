from datetime import datetime, date
from typing import Optional, Any
from backend.app.database.db import db

class ProviderService:
    @staticmethod
    def get_requests(provider_id: str = "provider-1") -> list[dict[str, Any]]:
        all_b = db.get_all_bookings()
        # Incoming requests are pending_provider or approved (awaiting allocation)
        reqs = [
            b for b in all_b
            if b.get("provider_id") == provider_id and b.get("status") in ("pending_provider", "approved")
        ]
        return reqs

    @staticmethod
    def accept_request(booking_id: str, quantities: dict[str, int], provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")
            if booking["status"] != "pending_provider":
                raise ValueError(f"Cannot accept booking in '{booking['status']}' state")

            new_lines = []
            total = 0.0
            for line in booking.get("lines", []):
                eq_id = line["equipment_id"]
                accepted_qty = quantities.get(eq_id, line["quantity"])
                if accepted_qty > 0:
                    amount = line["rate"] * accepted_qty * line["hours"]
                    total += amount
                    new_lines.append({
                        "equipment_id": eq_id,
                        "name": line["name"],
                        "quantity": accepted_qty,
                        "rate": line["rate"],
                        "hours": line["hours"],
                        "amount": amount,
                    })

            if not new_lines:
                raise ValueError("At least one equipment unit must be accepted")

            booking["lines"] = new_lines
            booking["total"] = total
            booking["provider_reviewed"] = True
            booking["status"] = "pending_approval"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": provider_id,
                "action": "provider_accepted",
                "timestamp": datetime.now().isoformat(),
                "note": f"Provider accepted requisition. Total: ₹{total:,.2f}",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def reject_request(booking_id: str, reason: str, provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "rejected"
            booking["reason"] = reason

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": provider_id,
                "action": "provider_rejected",
                "timestamp": datetime.now().isoformat(),
                "note": f"Provider rejected request: {reason}",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def assign_units(booking_id: str, assignments: list[dict[str, Any]], provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking_assignments = []
            for item in assignments:
                eq_id = item.get("equipment_id")
                veh_id = item.get("vehicle_id")
                op_id = item.get("operator_id")

                v = next((veh for veh in db.vehicles if veh["id"] == veh_id), None)
                if v:
                    v["status"] = "assigned"

                op = next((o for o in db.operators if o["id"] == op_id), None)
                if op:
                    op["status"] = "assigned"

                booking_assignments.append({
                    "equipment_id": eq_id,
                    "vehicle_id": veh_id,
                    "operator_id": op_id,
                })

            booking["assignments"] = booking_assignments
            booking["status"] = "assigned"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": provider_id,
                "action": "units_assigned",
                "timestamp": datetime.now().isoformat(),
                "note": f"Assigned {len(booking_assignments)} vehicle/operator units",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def get_schedule(provider_id: str = "provider-1", target_date: Optional[str] = None) -> list[dict[str, Any]]:
        all_b = db.get_all_bookings()
        scheduled_statuses = {"assigned", "in_transit", "arrived", "working", "awaiting_end", "completed", "problem"}
        res = [
            b for b in all_b
            if b.get("provider_id") == provider_id and b.get("status") in scheduled_statuses
        ]
        if target_date:
            res = [b for b in res if b.get("date") == target_date]
        return res

    @staticmethod
    def get_fleet(provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            vehs = [v for v in db.vehicles if v.get("provider_id") == provider_id]
            ops = [o for o in db.operators if o.get("provider_id") == provider_id]
            free_vehs = len([v for v in vehs if v.get("status") == "available"])
            booked_vehs = len([v for v in vehs if v.get("status") == "assigned"])
            free_ops = len([o for o in ops if o.get("status") == "available"])
            booked_ops = len([o for o in ops if o.get("status") == "assigned"])

            return {
                "vehicles": vehs,
                "operators": ops,
                "counts": {
                    "total_vehicles": len(vehs),
                    "free_vehicles": free_vehs,
                    "booked_vehicles": booked_vehs,
                    "total_operators": len(ops),
                    "free_operators": free_ops,
                    "booked_operators": booked_ops,
                }
            }

    @staticmethod
    def save_equipment(data: dict[str, Any], provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            existing_id = data.get("id")
            if existing_id:
                veh = next((v for v in db.vehicles if v["id"] == existing_id), None)
                if not veh:
                    raise ValueError("Vehicle not found")
                veh.update(data)
                return veh
            else:
                new_id = f"vehicle-{len(db.vehicles) + 101}"
                new_veh = {
                    "id": new_id,
                    "provider_id": provider_id,
                    "equipment_id": data.get("equipment_id", "eq-2"),
                    "registration": data.get("registration", "MH 02 EQ 9999"),
                    "status": "available",
                    "model": data.get("model", "JCB 3DX EcoExpert"),
                    "category": data.get("category", "Earthmoving"),
                    "rate": float(data.get("rate", 1450.0)),
                    "overtime": float(data.get("overtime", 220.0)),
                    "depot": data.get("depot", "Depot Bandra West"),
                }
                db.vehicles.append(new_veh)
                return new_veh

    @staticmethod
    def get_profile(provider_id: str = "provider-1") -> dict[str, Any]:
        with db.lock:
            completed_bookings = [b for b in db.bookings if b.get("provider_id") == provider_id and b.get("status") == "completed"]
            active_bookings = [b for b in db.bookings if b.get("provider_id") == provider_id and b.get("status") in ("assigned", "in_transit", "arrived", "working")]
            
            settled = sum(b.get("total", 0.0) for b in completed_bookings)
            pending = sum(b.get("total", 0.0) for b in active_bookings)

            return {
                "name": "Mahalaxmi Earthmovers & Fleet",
                "owner": "Amit Desai",
                "phone": "+91 98201 44553",
                "depot": "Depot Bandra West, S.V. Road, Santacruz West",
                "gstin": "27AAECM4819M1ZV",
                "total_settled": settled if settled > 0 else 342800.0,
                "pending_clearance": pending if pending > 0 else 46500.0,
                "completed_shifts": len(completed_bookings) if len(completed_bookings) > 0 else 34,
            }
