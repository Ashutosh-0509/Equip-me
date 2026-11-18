import reflex as rx

from datetime import date, timedelta
from typing import TypedDict


class Equipment(TypedDict):
    id: str
    name: str
    category: str
    description: str
    rate: float
    image: str
    provider_id: str


class Line(TypedDict):
    equipment_id: str
    name: str
    quantity: int
    rate: float
    hours: int
    amount: float


class Assignment(TypedDict):
    equipment_id: str
    vehicle_id: str
    operator_id: str


class Booking(TypedDict):
    id: str
    contractor_id: str
    provider_id: str
    status: str
    date: str
    shift: str
    hours: int
    address: str
    ward: str
    latitude: str
    longitude: str
    work_order: str
    lines: list[Line]
    total: float
    assignments: list[Assignment]
    requested_lines: list[Line]
    requested_total: float
    provider_reviewed: bool
    start_pin: str
    end_pin: str
    started_at: str
    ended_at: str
    reason: str
    safety_confirmed: bool


class Identity(TypedDict):
    id: str
    role: str
    name: str
    company: str
    phone: str
    email: str


class Vehicle(TypedDict):
    id: str
    provider_id: str
    equipment_id: str
    registration: str
    status: str
    model: str
    category: str
    rate: float
    overtime: float
    depot: str


class Operator(TypedDict):
    id: str
    provider_id: str
    name: str
    phone: str
    license: str
    status: str


class Audit(TypedDict):
    id: str
    booking_id: str
    actor_id: str
    action: str
    timestamp: str
    note: str


class Dispute(TypedDict):
    id: str
    booking_id: str
    contractor_id: str
    category: str
    description: str
    status: str
    resolution: str
    created_at: str


CATALOGUE: list[Equipment] = [
    {
        "id": "eq-1",
        "name": "Heavy Excavator",
        "category": "Earthmoving",
        "description": "20T · Heavy digging & trenches",
        "rate": 1850.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAxODQnmf-_a6axH59jg-14YDySxIbycVMUIN7SRi2R5rZtDoM4cNRiyOgLkIsRzWIraLJSeAUHq0gE-42xsIRw9NV65FkSl0HF3b9ByHv5jvw-0w0yK4wwCBF5ICU3GSzYAFMOhaTrn5KpG_Ax58-l_Pb0dhDDmPFP2QpnWl_PP0BwpBqI9D_sA1gPkB_79McpnEmNF_N2wvSwuCIP3G9Yd52pNUxLID-6tyk4yv8vqbufIyfq-j4",
    },
    {
        "id": "eq-2",
        "name": "JCB 3DX Backhoe",
        "category": "Earthmoving",
        "description": "Loader + Backhoe multi-use",
        "rate": 1250.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuAlnSwNa5hpT93V59TjeNyCMTX1Xfzh5VqKvKcaqKx9M8PlyuXdGVNA-MQd-2dY39st7o7YtBCVP7hrBHJoMbtxdjwYNBZXTTzmzh7nX69-q9wrOQutK9yqzt9cp97HbU9o1o6a7uEnNqdwEfUCvdQgdmex-qjZGWiqNPCCH5-IUBEPycOfQBw6mK8T3xhMDG4pnWsRv3sR6qf-nYEbfm_ArmYcLGx7Zq7aJuBLvA",
    },
    {
        "id": "eq-3",
        "name": "16-Ton Tipper",
        "category": "Haulage",
        "description": "Muck & debris haulage",
        "rate": 1450.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuB6pCbpqficl0E3CtSSd9pGjLpuLdKgCgsUM0sL2KaW0bOCZx65TdgKuuHkUdKqdDVuRRdj5maD3disW_7xitCYdAaVCEWlQSJAzYHvaZu4NySSuo673Oo8FoSt_d2SL9Mhayfr-0RNsiMbT3DKGHVpqKx_E5UbOQWzQWNL_s3fl6zneSoAFp-VQqC6J8Cn3QF-2FvYpy3GugHlDzHuYN_sp9FxP1WDGLEhhX-p6g",
    },
    {
        "id": "eq-4",
        "name": "Soil Compactor",
        "category": "Compaction & RMC",
        "description": "11T Vibratory roller",
        "rate": 1150.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDyTX5SyMqsdOSH2Sn6I1pmqqk1XuP7yI2XAo9JcBy5mdzpJpJDlzIxSDb2WL7Bo2P24dqU6M9LXMWbdp4nlUaN6UuzsAPVnLyTaPv2aMp8zoK9ZmLAJyoskduyESApQ2jQGIhBY4cuh3KZn83nUBtHYNrSBsIaY4pzhLvvzSHtynYlAz6p7G3cEb7g2oBOUqnF8qJ_kHJzox6QVzUtZ27CLMcLna9caVlXl-hvFg",
    },
    {
        "id": "eq-5",
        "name": "Transit Mixer",
        "category": "Compaction & RMC",
        "description": "6 cu.m RMC Batching",
        "rate": 1700.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuCsdg-bu4_R20NmKzGy_qGMgVzM_yudhg0SuaBBIEz0uZxcOV6rLzExvuTWLDkocDQ12yEu2FN3IL6HosbCLzwye2_utl1MnFFVx_3mMcjaNe0dQldz2UAgGmNh54IVUcJzcN_RnExaPuLr3UO65zd8abhTYSIUvGuL-uNqtpkK4veXhpE-5m6QbfQXJ41oL0oaaioPSSWE7fVOMVp-bseNdg-xjeamKGeeQh48lw",
    },
    {
        "id": "eq-6",
        "name": "Hydra Crane",
        "category": "Cranes",
        "description": "14T Girder & Precast Lift",
        "rate": 2100.0,
        "provider_id": "provider-1",
        "image": "https://lh3.googleusercontent.com/aida-public/AB6AXuDMpkrAgFIa8g0lhMZIffe0zEsi2-_47b0CYbgQ5YVzaMuZ7jlQyRdyCNO4HnKriNwo3IHGqqmyeRcClgriu_x2pvoLkuWVxc134efly8kpEuZ2L8EGN9lj-r56SVnXq9fYE-e7EM1YfLGOtQWWr7bY4NkGXSIxxWMXi-35mqG8kmikF8R5DUIT2gxrmQ0jNG2oSiUkpPxdTt4wK90r3UdqBIFcSZr4jD24jUB6BA",
    },
]
IDENTITIES: list[Identity] = [
    {
        "id": "contractor-1",
        "role": "Contractor",
        "name": "Rajesh Patel",
        "company": "Patel Infrastructure Pvt. Ltd.",
        "phone": "+91 98201 44552",
        "email": "rajesh@example.test",
    },
    {
        "id": "provider-1",
        "role": "Provider",
        "name": "Amit Desai",
        "company": "Desai Earthmovers",
        "phone": "+91 98201 44553",
        "email": "amit@example.test",
    },
    {
        "id": "operator-1",
        "role": "Operator",
        "name": "Ramesh Solanki",
        "company": "Desai Earthmovers",
        "phone": "+91 98201 44554",
        "email": "ramesh@example.test",
    },
    {
        "id": "officer-1",
        "role": "Officer",
        "name": "Anita Joshi",
        "company": "BMC · H/West Ward",
        "phone": "+91 98201 44555",
        "email": "anita@example.test",
    },
]
CONTRACTORS: list[Identity] = [
    IDENTITIES[0],
    {
        "id": "contractor-2",
        "role": "Contractor",
        "name": "Rajesh Sharma",
        "company": "Sharma Infra & Co.",
        "phone": "+91 98201 44556",
        "email": "sharma@example.test",
    },
]
PROVIDERS: list[Identity] = [
    IDENTITIES[1],
    {
        "id": "provider-2",
        "role": "Provider",
        "name": "Neha Shah",
        "company": "Mumbai Plant Hire",
        "phone": "+91 98201 44557",
        "email": "neha@example.test",
    },
]
STATUSES = [
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
STATUS_LABELS = {
    "draft": "Draft",
    "pending_provider": "Awaiting provider",
    "pending_approval": "Awaiting BMC approval",
    "approved": "Approved · Allocation required",
    "assigned": "Vehicle & operator assigned",
    "in_transit": "On the way",
    "arrived": "Operator arrived at site",
    "working": "Work in progress",
    "awaiting_end": "Awaiting end-code handoff",
    "completed": "Completed",
    "rejected": "Rejected",
    "cancelled": "Cancelled",
    "problem": "Issue reported",
}
SHIFTS: dict[str, int] = {
    "Shift A · 08:00–16:00": 8,
    "Shift B · 16:00–00:00": 8,
    "Full day · 08:00–20:00": 12,
}
EMPTY_BOOKING: Booking = {
    "id": "",
    "contractor_id": "",
    "provider_id": "",
    "status": "draft",
    "date": "",
    "shift": "",
    "hours": 0,
    "address": "",
    "ward": "",
    "latitude": "",
    "longitude": "",
    "work_order": "",
    "lines": [],
    "total": 0.0,
    "assignments": [],
    "requested_lines": [],
    "requested_total": 0.0,
    "provider_reviewed": False,
    "start_pin": "",
    "end_pin": "",
    "started_at": "",
    "ended_at": "",
    "reason": "",
    "safety_confirmed": False,
}


def sample_fixtures() -> tuple[
    list[Booking], list[Vehicle], list[Operator], list[Audit], list[Dispute]
]:
    bookings: list[Booking] = []
    vehicles: list[Vehicle] = []
    operators: list[Operator] = []
    audits: list[Audit] = []
    for index, status in enumerate(STATUSES):
        equipment = CATALOGUE[index % 6]
        number = index + 1
        vehicle_id = f"vehicle-{number}"
        operator_id = (
            "operator-1"
            if index == 5
            else "operator-13"
            if index == 0
            else "operator-16"
            if status == "approved"
            else f"operator-{number}"
        )
        quantity = 2 if status == "completed" else 1
        day = date.today() + timedelta(
            days=-2
            if status in ("completed", "cancelled", "rejected")
            else 0
            if status
            in ("arrived", "working", "awaiting_end", "problem", "in_transit")
            else 1
        )
        line: Line = {
            "equipment_id": equipment["id"],
            "name": equipment["name"],
            "quantity": quantity,
            "rate": equipment["rate"],
            "hours": 8,
            "amount": equipment["rate"] * quantity * 8,
        }
        assigned = status in (
            "assigned",
            "in_transit",
            "arrived",
            "working",
            "awaiting_end",
            "completed",
            "problem",
        )
        bookings.append(
            {
                "id": f"BMC-{8840 + index}",
                "contractor_id": "contractor-1",
                "provider_id": "provider-1",
                "status": status,
                "date": day.isoformat(),
                "shift": list(SHIFTS)[0],
                "hours": 8,
                "address": "Plot 42-B, SV Road Extension, Opp. Milan Subway, Santacruz (West), Mumbai 400054",
                "ward": "H/West",
                "latitude": "19.0830",
                "longitude": "72.8370",
                "work_order": "WO-2026-8842 · Storm Water Drain Widening & Desilting",
                "lines": [line],
                "requested_lines": [dict(line)],
                "requested_total": line["amount"],
                "provider_reviewed": status
                not in {"draft", "pending_provider", "rejected"},
                "total": line["amount"],
                "assignments": [
                    {
                        "equipment_id": equipment["id"],
                        "vehicle_id": vehicle_id,
                        "operator_id": operator_id,
                    }
                ]
                if assigned
                else [],
                "start_pin": f"{8420 + index}",
                "end_pin": f"{6250 + index}",
                "started_at": f"{day.isoformat()}T08:00:00+05:30"
                if status in ("working", "awaiting_end", "completed")
                else "",
                "ended_at": f"{day.isoformat()}T16:00:00+05:30"
                if status == "completed"
                else "",
                "reason": "Site access not ready"
                if status == "cancelled"
                else "Equipment unavailable"
                if status == "rejected"
                else "Hydraulic leak reported"
                if status == "problem"
                else "",
                "safety_confirmed": status != "draft",
            }
        )
        vehicles.append(
            {
                "id": vehicle_id,
                "provider_id": "provider-1",
                "equipment_id": equipment["id"],
                "registration": f"MH 02 AB {4200 + index}",
                "status": "assigned"
                if assigned and status != "completed"
                else "available",
            }
        )
        operators.append(
            {
                "id": operator_id,
                "provider_id": "provider-1",
                "name": "Ramesh Solanki"
                if index == 5
                else [
                    "Suresh Patil",
                    "Imran Shaikh",
                    "Vijay More",
                    "Ganesh Jadhav",
                ][index % 4],
                "phone": "+91 98201 44554",
                "license": f"MH-OP-{1000 + index}",
                "status": "assigned"
                if assigned and status != "completed"
                else "available",
            }
        )
        audits.append(
            {
                "id": f"audit-{number}",
                "booking_id": bookings[-1]["id"],
                "actor_id": "officer-1",
                "action": status,
                "timestamp": f"{day.isoformat()}T07:45:00+05:30",
                "note": "Sample lifecycle evidence",
            }
        )
    completed = bookings[8]
    completed["assignments"].append(
        {
            "equipment_id": completed["lines"][0]["equipment_id"],
            "vehicle_id": "vehicle-15",
            "operator_id": "operator-15",
        }
    )
    vehicles.append(
        {
            "id": "vehicle-15",
            "provider_id": "provider-1",
            "equipment_id": completed["lines"][0]["equipment_id"],
            "registration": "MH 02 AB 4215",
            "status": "available",
        }
    )
    operators.append(
        {
            "id": "operator-15",
            "provider_id": "provider-1",
            "name": "Dinesh Pawar",
            "phone": "+91 98201 44554",
            "license": "MH-OP-1015",
            "status": "available",
        }
    )
    disputes: list[Dispute] = [
        {
            "id": "dispute-1",
            "booking_id": "BMC-8851",
            "contractor_id": "contractor-1",
            "category": "Breakdown",
            "description": "Hydraulic leak reported; equipment stopped safely.",
            "status": "open",
            "resolution": "",
            "created_at": f"{date.today().isoformat()}T09:20:00+05:30",
        }
    ]
    for vehicle in vehicles:
        equipment = next(
            e for e in CATALOGUE if e["id"] == vehicle["equipment_id"]
        )
        vehicle.update(
            model=equipment["name"],
            category=equipment["category"],
            rate=equipment["rate"],
            overtime=equipment["rate"],
            depot="Bandra West, S.V. Road depot",
        )
    return bookings, vehicles, operators, audits, disputes
