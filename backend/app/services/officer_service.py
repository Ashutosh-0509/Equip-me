import csv
import io
from datetime import datetime
from typing import Optional, Any
from backend.app.database.db import db

class OfficerService:
    @staticmethod
    def get_dashboard() -> dict[str, Any]:
        all_b = db.get_all_bookings()
        waiting_approval = [b for b in all_b if b.get("status") == "pending_approval"]
        not_matched = [b for b in all_b if b.get("status") == "pending_provider"]
        active_today = [b for b in all_b if b.get("status") in ("assigned", "in_transit", "arrived", "working", "awaiting_end")]
        problems_open = [b for b in all_b if b.get("status") == "problem"]
        open_disputes = [d for d in db.disputes if d.get("status") == "open"]

        return {
            "control_room": "Ward G/N Control Room",
            "officer": {
                "name": "Er. Amit Deshmukh",
                "title": "Ward Executive Engineer (Machinery Pool)",
                "ward": "Ward G/North (Dharavi / Kurla)",
                "status": "Online · Live Telematics",
            },
            "alerts_count": len(waiting_approval) + len(problems_open),
            "pulse": {
                "waiting_approval": len(waiting_approval),
                "not_matched": len(not_matched),
                "active_today": len(active_today),
                "problems_open": len(problems_open) + len(open_disputes),
            },
            "urgent_queue": waiting_approval[:5],
            "active_deployments": active_today[:5],
            "open_disputes": open_disputes,
        }

    @staticmethod
    def get_requests(search: Optional[str] = None, status: Optional[str] = None, ward: Optional[str] = None) -> list[dict[str, Any]]:
        all_b = db.get_all_bookings()

        if status and status.lower() != "all":
            s = status.lower()
            if s == "needs_approval" or s == "needs approval":
                all_b = [b for b in all_b if b.get("status") == "pending_approval"]
            elif s == "not_matched" or s == "not matched":
                all_b = [b for b in all_b if b.get("status") == "pending_provider"]
            elif s == "active":
                all_b = [b for b in all_b if b.get("status") in ("assigned", "in_transit", "arrived", "working", "awaiting_end")]
            elif s == "completed":
                all_b = [b for b in all_b if b.get("status") == "completed"]
            elif s == "issues":
                all_b = [b for b in all_b if b.get("status") in ("problem", "rejected", "cancelled")]
            else:
                all_b = [b for b in all_b if b.get("status") == s]

        if ward and ward.lower() != "all":
            all_b = [b for b in all_b if ward.lower() in b.get("ward", "").lower()]

        if search:
            q = search.lower().strip()
            all_b = [
                b for b in all_b
                if q in b.get("id", "").lower()
                or q in b.get("work_order", "").lower()
                or q in b.get("address", "").lower()
                or q in b.get("contractor_company", "").lower()
                or q in b.get("provider_company", "").lower()
            ]

        return all_b

    @staticmethod
    def approve_booking(booking_id: str, note: str = "Requisition approved by Municipal Control Room.", officer_id: str = "officer-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            # Changes status to approved
            booking["status"] = "approved"

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": officer_id,
                "action": "approved",
                "timestamp": datetime.now().isoformat(),
                "note": note,
            })

            return db.enrich_booking(booking)

    @staticmethod
    def reject_booking(booking_id: str, reason: str, officer_id: str = "officer-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            booking["status"] = "rejected"
            booking["reason"] = reason

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": officer_id,
                "action": "officer_rejected",
                "timestamp": datetime.now().isoformat(),
                "note": f"Requisition rejected by officer: {reason}",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def reassign_booking(booking_id: str, reason: str, assignments: list[dict[str, Any]], officer_id: str = "officer-1") -> dict[str, Any]:
        with db.lock:
            booking = next((b for b in db.bookings if b["id"] == booking_id), None)
            if not booking:
                raise ValueError("Booking not found")

            # Release previous assignments
            for a in booking.get("assignments", []):
                v = next((veh for veh in db.vehicles if veh["id"] == a.get("vehicle_id")), None)
                if v:
                    v["status"] = "available"
                op = next((o for o in db.operators if o["id"] == a.get("operator_id")), None)
                if op:
                    op["status"] = "available"

            new_assignments = []
            for item in assignments:
                veh_id = item.get("vehicle_id")
                op_id = item.get("operator_id")
                eq_id = item.get("equipment_id")
                
                v = next((veh for veh in db.vehicles if veh["id"] == veh_id), None)
                if v:
                    v["status"] = "assigned"
                op = next((o for o in db.operators if o["id"] == op_id), None)
                if op:
                    op["status"] = "assigned"

                new_assignments.append({
                    "equipment_id": eq_id,
                    "vehicle_id": veh_id,
                    "operator_id": op_id,
                })

            booking["assignments"] = new_assignments
            booking["status"] = "assigned"
            booking["reason"] = ""

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": booking_id,
                "actor_id": officer_id,
                "action": "fleet_reassigned",
                "timestamp": datetime.now().isoformat(),
                "note": f"Fleet reassigned due to: {reason}",
            })

            return db.enrich_booking(booking)

    @staticmethod
    def get_directory(tab: str = "providers", search: Optional[str] = None) -> dict[str, Any]:
        with db.lock:
            providers_list = [
                {
                    "id": "provider-1",
                    "name": "Mahalaxmi Earthmovers & Fleet",
                    "contact_person": "Amit Desai",
                    "depot": "Kurla West Depot · BMC-WR-001",
                    "grade": "Grade A · 4.8",
                    "fleet_count": 12,
                    "compliance": "100%",
                    "phone": "+91 98201 44553",
                    "status": "Active",
                },
                {
                    "id": "provider-2",
                    "name": "Bandra Infra Heavy Machineries",
                    "contact_person": "Neha Shah",
                    "depot": "Bandra East Depot · BMC-WR-004",
                    "grade": "Grade A · 4.7",
                    "fleet_count": 8,
                    "compliance": "98%",
                    "phone": "+91 98201 44557",
                    "status": "Active",
                },
                {
                    "id": "provider-3",
                    "name": "Sion Civil & Heavy Logistics",
                    "contact_person": "Sanjay Mehta",
                    "depot": "Sion Municipal Yard · BMC-CR-009",
                    "grade": "Grade B · 4.2",
                    "fleet_count": 15,
                    "compliance": "94%",
                    "phone": "+91 98201 44558",
                    "status": "Papers Expired",
                },
            ]

            contractors_list = [
                {
                    "id": "contractor-1",
                    "name": "Patel Infrastructure Pvt. Ltd.",
                    "contact_person": "Rajesh Patel",
                    "registration_no": "BMC/CIVIL/2021/489",
                    "grade": "Class 1 (Unlimited)",
                    "active_sites": 3,
                    "compliance": "100%",
                    "phone": "+91 98201 44552",
                },
                {
                    "id": "contractor-2",
                    "name": "Sharma Infra & Co.",
                    "contact_person": "Rajesh Sharma",
                    "registration_no": "BMC/CIVIL/2019/312",
                    "grade": "Class 1 (Roads & SWD)",
                    "active_sites": 2,
                    "compliance": "97%",
                    "phone": "+91 98201 44556",
                },
                {
                    "id": "contractor-3",
                    "name": "Mehta Constructions Ltd.",
                    "contact_person": "Mahesh Shinde",
                    "registration_no": "BMC/CIVIL/2023/108",
                    "grade": "Class 2 (Bridges)",
                    "active_sites": 1,
                    "compliance": "96%",
                    "phone": "+91 98201 44559",
                },
            ]

            if search:
                q = search.lower().strip()
                providers_list = [p for p in providers_list if q in p["name"].lower() or q in p["depot"].lower()]
                contractors_list = [c for c in contractors_list if q in c["name"].lower()]

            return {
                "stats": {
                    "registered_providers": 42,
                    "civil_contractors": 18,
                    "compliance_rate": "98.4%",
                },
                "providers": providers_list,
                "contractors": contractors_list,
            }

    @staticmethod
    def get_disputes() -> list[dict[str, Any]]:
        with db.lock:
            return list(db.disputes)

    @staticmethod
    def resolve_dispute(dispute_id: str, note: str, officer_id: str = "officer-1") -> dict[str, Any]:
        with db.lock:
            dispute = next((d for d in db.disputes if d["id"] == dispute_id), None)
            if not dispute:
                raise ValueError("Dispute not found")

            dispute["status"] = "resolved"
            dispute["resolution"] = note

            db.audits.append({
                "id": f"audit-{len(db.audits) + 1}",
                "booking_id": dispute.get("booking_id", ""),
                "actor_id": officer_id,
                "action": "dispute_resolved",
                "timestamp": datetime.now().isoformat(),
                "note": f"Dispute {dispute_id} resolved: {note}",
            })

            return dispute

    @staticmethod
    def export_csv() -> str:
        all_b = db.get_all_bookings()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Booking ID", "Contractor", "Provider", "Status", "Date", "Shift",
            "Ward", "Work Order", "Equipment", "Quantity", "Total Amount (INR)",
            "Start PIN", "Started At", "Ended At"
        ])
        for b in all_b:
            lines_summary = ", ".join(f"{l.get('quantity')}x {l.get('name')}" for l in b.get("lines", []))
            writer.writerow([
                b.get("id"),
                b.get("contractor_company"),
                b.get("provider_company"),
                b.get("status_label"),
                b.get("date"),
                b.get("shift"),
                b.get("ward"),
                b.get("work_order"),
                lines_summary,
                sum(l.get("quantity", 1) for l in b.get("lines", [])),
                b.get("total"),
                b.get("start_pin"),
                b.get("started_at"),
                b.get("ended_at"),
            ])
        return output.getvalue()
