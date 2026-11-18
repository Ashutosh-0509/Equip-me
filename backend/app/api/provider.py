from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.app.schemas.domain_schemas import AcceptRequest, RejectRequest, ConfirmAssignmentRequest, SaveVehicleRequest
from backend.app.services.provider_service import ProviderService

router = APIRouter(prefix="/provider", tags=["Provider"])

@router.get("/requests")
def get_requests(provider_id: Optional[str] = "provider-1"):
    return ProviderService.get_requests(provider_id)

@router.post("/requests/{booking_id}/accept")
def accept_request(booking_id: str, data: AcceptRequest):
    try:
        return ProviderService.accept_request(booking_id, data.quantities)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/requests/{booking_id}/reject")
def reject_request(booking_id: str, data: RejectRequest):
    try:
        return ProviderService.reject_request(booking_id, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/assign/{booking_id}")
def assign_units(booking_id: str, data: ConfirmAssignmentRequest):
    try:
        assignments_dict = [a.model_dump() for a in data.assignments]
        return ProviderService.assign_units(booking_id, assignments_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/schedule")
def get_schedule(date: Optional[str] = None):
    return ProviderService.get_schedule(target_date=date)

@router.get("/fleet")
def get_fleet():
    return ProviderService.get_fleet()

@router.post("/equipment")
def save_equipment(data: SaveVehicleRequest):
    try:
        return ProviderService.save_equipment(data.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
def get_profile():
    return ProviderService.get_profile()
