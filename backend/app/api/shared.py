from fastapi import APIRouter
from backend.app.database.db import db

router = APIRouter(prefix="/shared", tags=["Shared"])

@router.get("/health")
def health_check():
    return {"status": "ok", "app": "BMC Heavy Logix Unified API", "version": "1.0.0"}

@router.post("/reset")
def reset_demo():
    db.reset()
    return {"status": "success", "message": "Demo data successfully reset to pristine state"}

@router.get("/overview")
def get_overview():
    all_b = db.get_all_bookings()
    return {
        "total_bookings": len(all_b),
        "pending_provider": len([b for b in all_b if b.get("status") == "pending_provider"]),
        "pending_approval": len([b for b in all_b if b.get("status") == "pending_approval"]),
        "approved": len([b for b in all_b if b.get("status") == "approved"]),
        "active": len([b for b in all_b if b.get("status") in ("assigned", "in_transit", "arrived", "working")]),
        "completed": len([b for b in all_b if b.get("status") == "completed"]),
        "problems": len([b for b in all_b if b.get("status") == "problem"]),
    }
