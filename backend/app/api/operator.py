from fastapi import APIRouter, HTTPException
from backend.app.schemas.domain_schemas import OperatorStartRequest, OperatorEndRequest, OperatorReportRequest, UpdateOperatorPhoneRequest
from backend.app.services.operator_service import OperatorService

router = APIRouter(prefix="/operator", tags=["Operator"])

@router.get("/today")
def get_today_assignment():
    return OperatorService.get_today_assignment()

@router.post("/transit/{booking_id}")
def start_transit(booking_id: str):
    try:
        return OperatorService.start_transit(booking_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/arrive/{booking_id}")
def mark_arrived(booking_id: str):
    try:
        return OperatorService.mark_arrived(booking_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify_start/{booking_id}")
def verify_start(booking_id: str, data: OperatorStartRequest):
    try:
        return OperatorService.verify_start_code(booking_id, data.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/request_end/{booking_id}")
def request_end(booking_id: str):
    try:
        return OperatorService.request_end(booking_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify_end/{booking_id}")
def verify_end(booking_id: str, data: OperatorEndRequest):
    try:
        return OperatorService.verify_end_code(booking_id, data.code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/report_issue")
def report_issue(data: OperatorReportRequest):
    if not data.booking_id:
        today_data = OperatorService.get_today_assignment()
        if today_data.get("current_assignment"):
            data.booking_id = today_data["current_assignment"]["id"]
        else:
            raise HTTPException(status_code=400, detail="No active booking to report issue for")

    try:
        return OperatorService.report_issue(data.booking_id, data.category, data.description)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/history")
def get_history():
    return OperatorService.get_history()

@router.get("/profile")
def get_profile():
    return OperatorService.get_profile()
