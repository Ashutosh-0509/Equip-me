from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.app.schemas.domain_schemas import BookingCreateRequest, BookingCancelRequest, BookingDisputeRequest
from backend.app.services.contractor_service import ContractorService

router = APIRouter(prefix="/contractor", tags=["Contractor"])

@router.get("/catalogue")
def get_catalogue(category: Optional[str] = None, search: Optional[str] = None):
    return ContractorService.get_catalogue(category, search)

@router.get("/bookings")
def get_bookings(status: Optional[str] = None, contractor_id: Optional[str] = "contractor-1"):
    return ContractorService.get_bookings(contractor_id, status)

@router.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    booking = ContractorService.get_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.post("/bookings")
def create_booking(data: BookingCreateRequest):
    try:
        return ContractorService.create_booking(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bookings/{booking_id}/cancel")
def cancel_booking(booking_id: str, data: BookingCancelRequest):
    try:
        return ContractorService.cancel_booking(booking_id, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bookings/{booking_id}/dispute")
def report_dispute(booking_id: str, data: BookingDisputeRequest):
    try:
        return ContractorService.report_dispute(booking_id, data.category, data.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
def get_profile():
    return {
        "company": "Sharma Infra & Co.",
        "contact_person": "Rajesh Sharma",
        "phone": "+91 98201 44512",
        "email": "contact@sharmainfra.test",
        "registration_no": "BMC/CIVIL/2019/312",
        "active_tasks": 1,
        "completed_tasks": 48,
        "ward": "Ward H/West",
        "compliance": "100%",
    }
