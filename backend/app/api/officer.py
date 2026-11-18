from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from typing import Optional
from backend.app.schemas.domain_schemas import OfficerApproveRequest, OfficerRejectRequest, OfficerReassignRequest, OfficerResolveDisputeRequest
from backend.app.services.officer_service import OfficerService

router = APIRouter(prefix="/officer", tags=["Officer"])

@router.get("/dashboard")
def get_dashboard():
    return OfficerService.get_dashboard()

@router.get("/requests")
def get_requests(search: Optional[str] = None, status: Optional[str] = None, ward: Optional[str] = None):
    return OfficerService.get_requests(search, status, ward)

@router.post("/bookings/{booking_id}/approve")
def approve_booking(booking_id: str, data: OfficerApproveRequest):
    try:
        return OfficerService.approve_booking(booking_id, data.note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bookings/{booking_id}/reject")
def reject_booking(booking_id: str, data: OfficerRejectRequest):
    try:
        return OfficerService.reject_booking(booking_id, data.reason)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bookings/{booking_id}/reassign")
def reassign_booking(booking_id: str, data: OfficerReassignRequest):
    try:
        assignments_dict = [a.model_dump() for a in data.assignments]
        return OfficerService.reassign_booking(booking_id, data.reason, assignments_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/directory")
def get_directory(tab: Optional[str] = "providers", search: Optional[str] = None):
    return OfficerService.get_directory(tab, search)

@router.get("/disputes")
def get_disputes():
    return OfficerService.get_disputes()

@router.post("/disputes/{dispute_id}/resolve")
def resolve_dispute(dispute_id: str, data: OfficerResolveDisputeRequest):
    try:
        return OfficerService.resolve_dispute(dispute_id, data.note)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/export")
def export_csv():
    csv_data = OfficerService.export_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=bmc_heavy_logix_report.csv"}
    )
