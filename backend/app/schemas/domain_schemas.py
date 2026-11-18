from pydantic import BaseModel, Field
from typing import Optional, Any

class LineItem(BaseModel):
    equipment_id: str
    name: str
    quantity: int
    rate: float
    hours: int
    amount: float

class AssignmentItem(BaseModel):
    equipment_id: str
    vehicle_id: str
    operator_id: str
    vehicle_model: Optional[str] = None
    vehicle_reg: Optional[str] = None
    operator_name: Optional[str] = None
    operator_phone: Optional[str] = None

class Booking(BaseModel):
    id: str
    contractor_id: str
    contractor_name: Optional[str] = None
    contractor_company: Optional[str] = None
    provider_id: str
    provider_name: Optional[str] = None
    provider_company: Optional[str] = None
    status: str
    status_label: Optional[str] = None
    date: str
    shift: str
    hours: int
    address: str
    ward: str
    latitude: str
    longitude: str
    work_order: str
    lines: list[LineItem] = []
    total: float
    assignments: list[AssignmentItem] = []
    requested_lines: list[LineItem] = []
    requested_total: float
    provider_reviewed: bool = False
    start_pin: str = ""
    end_pin: str = ""
    started_at: str = ""
    ended_at: str = ""
    reason: str = ""
    safety_confirmed: bool = False

class BookingCreateRequest(BaseModel):
    equipment_id: str
    quantity: int = Field(default=1, ge=1, le=10)
    date: str
    shift: str
    hours: int = 8
    address: str
    ward: str
    latitude: Optional[str] = "19.0830"
    longitude: Optional[str] = "72.8370"
    work_order: str
    safety_confirmed: bool = True

class BookingCancelRequest(BaseModel):
    reason: str
    confirm: bool = True

class BookingDisputeRequest(BaseModel):
    category: str
    description: str

class EquipmentItem(BaseModel):
    id: str
    name: str
    category: str
    description: str
    rate: float
    image: str
    provider_id: str

class VehicleItem(BaseModel):
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

class OperatorItem(BaseModel):
    id: str
    provider_id: str
    name: str
    phone: str
    license: str
    status: str

class AuditItem(BaseModel):
    id: str
    booking_id: str
    actor_id: str
    action: str
    timestamp: str
    note: str

class DisputeItem(BaseModel):
    id: str
    booking_id: str
    contractor_id: str
    contractor_name: Optional[str] = None
    category: str
    description: str
    status: str
    resolution: str = ""
    created_at: str

class IdentityItem(BaseModel):
    id: str
    role: str
    name: str
    company: str
    phone: str
    email: str

class AcceptRequest(BaseModel):
    quantities: dict[str, int]  # equipment_id -> quantity

class RejectRequest(BaseModel):
    reason: str
    confirm: bool = True

class UnitAssignment(BaseModel):
    unit_key: str
    equipment_id: str
    vehicle_id: str
    operator_id: str

class ConfirmAssignmentRequest(BaseModel):
    assignments: list[UnitAssignment]

class SaveVehicleRequest(BaseModel):
    id: Optional[str] = None
    equipment_id: str
    registration: str
    model: str
    category: str
    rate: float
    overtime: float
    depot: str
    status: Optional[str] = "available"

class OperatorStartRequest(BaseModel):
    code: str
    safety_confirmed: bool = True

class OperatorEndRequest(BaseModel):
    code: str
    inspection_confirmed: bool = True

class OperatorReportRequest(BaseModel):
    booking_id: Optional[str] = None
    category: str
    description: str

class UpdateOperatorPhoneRequest(BaseModel):
    phone: str

class OfficerApproveRequest(BaseModel):
    site_verified: bool = True
    work_order_verified: bool = True
    provider_verified: bool = True
    safety_verified: bool = True
    partial_ack: Optional[bool] = False
    note: str = "Verified and approved according to municipal standard protocols."

class OfficerRejectRequest(BaseModel):
    reason: str
    confirm: bool = True

class OfficerReassignRequest(BaseModel):
    reason: str
    confirm: bool = True
    assignments: list[UnitAssignment]

class OfficerResolveDisputeRequest(BaseModel):
    note: str
    confirm: bool = True

class OfficerNoteRequest(BaseModel):
    note: str
