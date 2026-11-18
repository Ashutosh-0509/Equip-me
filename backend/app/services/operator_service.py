from datetime import datetime
from typing import Optional, Any
from backend.app.database.db import db

class OperatorService:
    @staticmethod
    def get_today_assignment(operator_id: str = "operator-1") -> dict[str, Any]:
        all_b = db.get_all_bookings()
        # Find bookings where operator is assigned
        op_bookings = []
        for b in all_b:
            for a in b.get("assignments", []):
                if a.get("operator_id") == operator_id:
                    op_bookings.append(b)
                    break

        # Priority order: working > arrived > in_transit > assigned > awaiting_end > others
        priority = {
            "working": 1,
            "arrived": 2,
            "in_transit": 3,
            "assigned": 4,
            "awaiting_end": 5,
        }

        active_b = [b for b in op_bookings if b.get("status") in priority]
        active_b.sort(key=lambda x: priority.get(x.get("status", ""), 99))

        current = active_b[0] if active_b else None
        
        # If no active assignment found, fall back to first arrived or assigned booking
        if not current:
            for b in all_b:
                if b.get("status") in ("arrived", "assigned", "in_transit", "working"):
                    current = b
                    break

        # Next shift
        next_shift = {
            "time": "Tomorrow · 08:30 AM",
            "equipment": "Tata Hitachi EX200",
            "site": "Dharavi Link Road Desilting Works · Sector 5",
            "shift_lead": "Rajesh V. Sharma",
        }

        return {
            "operator": {
                "id": operator_id,
                "name": "Ramesh Solanki",
                "phone": "+91 98201 44554",
                "license": "MH-OP-1005",
                "status": "On Duty",
            },
            "current_assignment": current,
            "next_shift": next_shift,
        }

    @staticmethod
    def start_transit(booking_id: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "in_transit"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": operator_id,
                "action": "transit_started",
                "timestamp": datetime.now().isoformat(),
                "note": "Operator started transit to job site",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def mark_arrived(booking_id: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "arrived"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": operator_id,
                "action": "arrived_at_site",
                "timestamp": datetime.now().isoformat(),
                "note": "Operator reported arrival at work site",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def verify_start_code(booking_id: str, code: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            if booking.get("start_pin") and booking["start_pin"] != code.strip():
                raise ValueError(f"Invalid PIN '{code}'. Check the 4-digit code shown on the Contractor's Live Booking screen.")

            booking["status"] = "working"
            booking["started_at"] = datetime.now().isoformat()

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": operator_id,
                "action": "machine_started",
                "timestamp": datetime.now().isoformat(),
                "note": "4-digit arrival PIN verified. Machine shift commenced.",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def request_end(booking_id: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "awaiting_end"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": operator_id,
                "action": "end_code_requested",
                "timestamp": datetime.now().isoformat(),
                "note": "Operator requested shift completion handoff code",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def verify_end_code(booking_id: str, code: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            if booking.get("end_pin") and booking["end_pin"] != code.strip():
                raise ValueError("Invalid End PIN. Please obtain handoff code from Site Manager.")

            booking["status"] = "completed"
            booking["ended_at"] = datetime.now().isoformat()

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
                "actor_id": operator_id,
                "action": "shift_completed",
                "timestamp": datetime.now().isoformat(),
                "note": "Shift successfully completed and verified.",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def report_issue(booking_id: str, category: str, description: str, operator_id: str = "operator-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "problem"
            booking["reason"] = description

            dispute = {
                "id": f"dispute-{len(db.disputes) + 1}",
                "booking_id": booking_id,
                "contractor_id": booking.get("contractor_id", "contractor-1"),
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
                "actor_id": operator_id,
                "action": "operator_incident_reported",
                "timestamp": datetime.now().isoformat(),
                "note": f"Incident reported by operator: {description}",
            })

            return dispute

    @staticmethod
    def get_history(operator_id: str = "operator-1") -> list[dict[str, Any]]:
        all_b = db.get_all_bookings()
        return [b for b in all_b if b.get("status") in ("completed", "working", "problem", "arrived")]

    @staticmethod
    def get_profile(operator_id: str = "operator-1") -> dict[str, Any]:
        return {
            "id": operator_id,
            "name": "Ramesh Solanki",
            "phone": "+91 98201 44554",
            "license": "MH-OP-1005",
            "provider": "Mahalaxmi Earthmovers & Fleet",
            "status": "On Duty",
            "total_shifts": 48,
            "safety_rating": 4.9,
        }
