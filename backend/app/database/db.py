import copy
import threading
from datetime import date, datetime, timedelta
from typing import Optional, Any

# Initial Catalogue Definitions
CATALOGUE = [
    {
        "id": "eq-1",
        "name": "Heavy Excavator",
        "category": "Earthmoving",
        "description": "20T · Heavy digging & trenches",
        "rate": 1850.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/excavator.svg",
    },
    {
        "id": "eq-2",
        "name": "JCB 3DX Backhoe",
        "category": "Earthmoving",
        "description": "Loader + Backhoe multi-use",
        "rate": 1450.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/backhoe.svg",
    },
    {
        "id": "eq-3",
        "name": "16-Ton Tipper",
        "category": "Haulage",
        "description": "Muck & debris haulage",
        "rate": 1100.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/tipper.svg",
    },
    {
        "id": "eq-4",
        "name": "Soil Compactor",
        "category": "Compaction & RMC",
        "description": "11T Vibratory roller",
        "rate": 1150.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/compactor.svg",
    },
    {
        "id": "eq-5",
        "name": "Transit Mixer",
        "category": "Compaction & RMC",
        "description": "6 cu.m RMC Batching",
        "rate": 1250.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/mixer.svg",
    },
    {
        "id": "eq-6",
        "name": "Hydra Crane",
        "category": "Cranes",
        "description": "14T Girder & Precast Lift",
        "rate": 2150.0,
        "provider_id": "provider-1",
        "image": "/assets/machinery/crane.svg",
    },
]

IDENTITIES = [
    {
        "id": "contractor-1",
        "role": "Contractor",
        "name": "Rajesh Patel",
        "company": "Patel Infrastructure Pvt. Ltd.",
        "phone": "+91 98201 44552",
        "email": "rajesh@patelinfra.test",
    },
    {
        "id": "provider-1",
        "role": "Provider",
        "name": "Amit Desai",
        "company": "Mahalaxmi Earthmovers & Fleet",
        "phone": "+91 98201 44553",
        "email": "amit@mahalaxmifleet.test",
    },
    {
        "id": "operator-1",
        "role": "Operator",
        "name": "Ramesh Solanki",
        "company": "Mahalaxmi Earthmovers & Fleet",
        "phone": "+91 98201 44554",
        "email": "ramesh@operator.test",
    },
    {
        "id": "officer-1",
        "role": "Officer",
        "name": "Er. Amit Deshmukh",
        "company": "BMC · Ward G/N Control Room",
        "phone": "+91 98201 44555",
        "email": "amit.deshmukh@mcgm.gov.in",
    },
]

CONTRACTORS = [
    IDENTITIES[0],
    {
        "id": "contractor-2",
        "role": "Contractor",
        "name": "Rajesh Sharma",
        "company": "Sharma Infra & Co.",
        "phone": "+91 98201 44556",
        "email": "sharma@sharmainfra.test",
    },
]

PROVIDERS = [
    IDENTITIES[1],
    {
        "id": "provider-2",
        "role": "Provider",
        "name": "Bandra Infra Heavy Machineries",
        "company": "Bandra Infra Heavy Machineries",
        "phone": "+91 98201 44557",
        "email": "dispatch@bandrainfra.test",
    },
]

STATUS_LABELS = {
    "draft": "Draft",
    "pending_provider": "Awaiting Provider",
    "pending_approval": "Awaiting Approval",
    "approved": "Approved · Needs Allocation",
    "assigned": "Assigned",
    "in_transit": "In Transit",
    "arrived": "Arrived at Site",
    "working": "Work in Progress",
    "awaiting_end": "Awaiting End Code",
    "completed": "Completed",
    "rejected": "Rejected",
    "cancelled": "Cancelled",
    "problem": "Dispute / Breakdown",
}

SHIFTS = {
    "Shift A · 08:00–16:00": 8,
    "Shift B · 16:00–00:00": 8,
    "Full day · 08:00–20:00": 12,
}

class InMemoryDB:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.catalogue = copy.deepcopy(CATALOGUE)
            self.identities = copy.deepcopy(IDENTITIES)
            self.contractors = copy.deepcopy(CONTRACTORS)
            self.providers = copy.deepcopy(PROVIDERS)
            self.status_labels = copy.deepcopy(STATUS_LABELS)
            self.shifts = copy.deepcopy(SHIFTS)
            
            # Generate fresh fixtures
            self.bookings = []
            self.vehicles = []
            self.operators = []
            self.audits = []
            self.disputes = []

            statuses = [
                "draft",
                "pending_provider",
                "pending_approval",
                "assigned",
                "in_transit",
                "arrived",
                "working",
                "awaiting_end",
                "completed",
                "rejected",
                "cancelled",
                "problem",
                "approved",
            ]

            today = date.today()

            for index, status in enumerate(statuses):
                eq = self.catalogue[index % 6]
                num = index + 1
                veh_id = f"vehicle-{num}"
                op_id = "operator-1" if index == 5 else f"operator-{num}"
                qty = 2 if status in ("completed", "pending_approval") else 1
                
                if status in ("completed", "cancelled", "rejected"):
                    day = today - timedelta(days=2)
                elif status in ("arrived", "working", "awaiting_end", "problem", "in_transit"):
                    day = today
                else:
                    day = today + timedelta(days=1)

                line = {
                    "equipment_id": eq["id"],
                    "name": eq["name"],
                    "quantity": qty,
                    "rate": eq["rate"],
                    "hours": 8,
                    "amount": eq["rate"] * qty * 8,
                }
                
                is_assigned = status in (
                    "assigned", "in_transit", "arrived", "working", "awaiting_end", "completed", "problem"
                )

                assignments = []
                if is_assigned:
                    for u in range(qty):
                        assignments.append({
                            "equipment_id": eq["id"],
                            "vehicle_id": veh_id if u == 0 else f"vehicle-{num}-alt",
                            "operator_id": op_id if u == 0 else f"operator-{num}-alt",
                        })

                self.bookings.append({
                    "id": f"BMC-{8840 + index}",
                    "contractor_id": "contractor-1" if index % 2 == 0 else "contractor-2",
                    "provider_id": "provider-1",
                    "status": status,
                    "date": day.isoformat(),
                    "shift": "Shift A · 08:00–16:00",
                    "hours": 8,
                    "address": "Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai 400054",
                    "ward": "H/West",
                    "latitude": "19.0830",
                    "longitude": "72.8370",
                    "work_order": "WO-2026-8842 · Storm Water Drain Widening & Desilting",
                    "lines": [line],
                    "total": line["amount"],
                    "assignments": assignments,
                    "requested_lines": [copy.deepcopy(line)],
                    "requested_total": line["amount"],
                    "provider_reviewed": status not in {"draft", "pending_provider", "rejected"},
                    "start_pin": f"{8420 + index}",
                    "end_pin": f"{6250 + index}",
                    "started_at": f"{day.isoformat()}T08:00:00+05:30" if status in ("working", "awaiting_end", "completed") else "",
                    "ended_at": f"{day.isoformat()}T16:00:00+05:30" if status == "completed" else "",
                    "reason": "Site access not ready" if status == "cancelled" else ("Equipment unavailable" if status == "rejected" else ("Hydraulic leak reported" if status == "problem" else "")),
                    "safety_confirmed": status != "draft",
                })

                self.vehicles.append({
                    "id": veh_id,
                    "provider_id": "provider-1",
                    "equipment_id": eq["id"],
                    "registration": f"MH 02 EQ {4490 + index}",
                    "status": "assigned" if is_assigned and status != "completed" else "available",
                    "model": f"{eq['name']} EcoExpert",
                    "category": eq["category"],
                    "rate": eq["rate"],
                    "overtime": round(eq["rate"] * 0.15, 2),
                    "depot": "Depot Bandra West, S.V. Road",
                })

                op_names = ["Ramesh Solanki", "Sunil Jadhav", "Mahesh Shinde", "Suresh Patil", "Vijay More", "Ganesh Pawar"]
                self.operators.append({
                    "id": op_id,
                    "provider_id": "provider-1",
                    "name": "Ramesh Solanki" if index == 5 or op_id == "operator-1" else op_names[index % len(op_names)],
                    "phone": f"+91 98201 {44550 + index}",
                    "license": f"MH-OP-{1000 + index}",
                    "status": "assigned" if is_assigned and status != "completed" else "available",
                })

                self.audits.append({
                    "id": f"audit-{num}",
                    "booking_id": f"BMC-{8840 + index}",
                    "actor_id": "officer-1",
                    "action": status,
                    "timestamp": f"{day.isoformat()}T07:45:00+05:30",
                    "note": f"Status initialized to {status}",
                })

            # Extra fleet units for assignments
            extra_vehicles = [
                {"id": "vehicle-101", "provider_id": "provider-1", "equipment_id": "eq-2", "registration": "MH-02-EQ-3812", "status": "available", "model": "JCB 3DX Plus 4WD", "category": "Earthmoving", "rate": 1450.0, "overtime": 220.0, "depot": "Depot Bandra West"},
                {"id": "vehicle-102", "provider_id": "provider-1", "equipment_id": "eq-2", "registration": "MH-02-EQ-4691", "status": "available", "model": "JCB 3DX EcoXpert", "category": "Earthmoving", "rate": 1450.0, "overtime": 220.0, "depot": "Depot Bandra West"},
                {"id": "vehicle-103", "provider_id": "provider-1", "equipment_id": "eq-1", "registration": "MH-02-AX-1802", "status": "available", "model": "Tata Hitachi EX200", "category": "Earthmoving", "rate": 1850.0, "overtime": 280.0, "depot": "Depot Bandra West"},
                {"id": "vehicle-104", "provider_id": "provider-1", "equipment_id": "eq-3", "registration": "MH-04-DE-2008", "status": "available", "model": "Tata Prima 16T Tipper", "category": "Haulage", "rate": 1100.0, "overtime": 180.0, "depot": "Depot Kurla West"},
            ]
            self.vehicles.extend(extra_vehicles)

            extra_operators = [
                {"id": "operator-101", "provider_id": "provider-1", "name": "Sunil Jadhav", "phone": "+91 98201 44521", "license": "MH-OP-2001", "status": "available"},
                {"id": "operator-102", "provider_id": "provider-1", "name": "Ramesh Pawar", "phone": "+91 98201 44522", "license": "MH-OP-2002", "status": "available"},
                {"id": "operator-103", "provider_id": "provider-1", "name": "Dinesh Gaikwad", "phone": "+91 98201 44523", "license": "MH-OP-2003", "status": "available"},
            ]
            self.operators.extend(extra_operators)

            # Sample disputes matching Reference Image 1 & 4
            self.disputes = [
                {
                    "id": "dispute-1",
                    "booking_id": "BMC-8851",
                    "contractor_id": "contractor-1",
                    "category": "Breakdown & Downtime Penalty",
                    "description": "Dispute between Sharma Infra and Sion Civil Yard regarding hydraulic hose failure on CAT 320D. Contested penalty: ₹48,500.",
                    "status": "open",
                    "resolution": "",
                    "created_at": f"{today.isoformat()}T09:20:00+05:30",
                },
                {
                    "id": "dispute-2",
                    "booking_id": "BMC-8846",
                    "contractor_id": "contractor-2",
                    "category": "Overtime Hours Discrepancy",
                    "description": "Operator logged 9.5 hrs vs 8.0 hrs claimed on Dharavi Pipeline culvert reinforcement. GPS ignition records compiled.",
                    "status": "open",
                    "resolution": "",
                    "created_at": f"{today.isoformat()}T11:15:00+05:30",
                },
            ]

    def enrich_booking(self, b: dict[str, Any]) -> dict[str, Any]:
        enriched = copy.deepcopy(b)
        # contractor info
        contractor = next((c for c in self.contractors if c["id"] == b.get("contractor_id")), None)
        if contractor:
            enriched["contractor_name"] = contractor["name"]
            enriched["contractor_company"] = contractor["company"]
        else:
            enriched["contractor_name"] = "Patel Infrastructure"
            enriched["contractor_company"] = "Patel Infrastructure Pvt. Ltd."

        # provider info
        provider = next((p for p in self.providers if p["id"] == b.get("provider_id")), None)
        if provider:
            enriched["provider_name"] = provider["name"]
            enriched["provider_company"] = provider["company"]
        else:
            enriched["provider_name"] = "Mahalaxmi Fleet"
            enriched["provider_company"] = "Mahalaxmi Earthmovers & Fleet"

        enriched["status_label"] = self.status_labels.get(b.get("status", ""), b.get("status", ""))

        # enrich assignments
        for a in enriched.get("assignments", []):
            v = next((veh for veh in self.vehicles if veh["id"] == a.get("vehicle_id")), None)
            if v:
                a["vehicle_model"] = v.get("model", "")
                a["vehicle_reg"] = v.get("registration", "")
            o = next((op for op in self.operators if op["id"] == a.get("operator_id")), None)
            if o:
                a["operator_name"] = o.get("name", "")
                a["operator_phone"] = o.get("phone", "")

        return enriched

    def get_all_bookings(self) -> list[dict[str, Any]]:
        with self.lock:
            return [self.enrich_booking(b) for b in self.bookings]

    def get_booking_by_id(self, booking_id: str) -> Optional[dict[str, Any]]:
        with self.lock:
            for b in self.bookings:
                if b["id"] == booking_id:
                    return self.enrich_booking(b)
            return None

db = InMemoryDB()
