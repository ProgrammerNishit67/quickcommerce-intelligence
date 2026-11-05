from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.export_service import export_report_to_bytes

router = APIRouter(prefix="/reports", tags=["Reporting & Exports"])

VALID_REPORTS = ["daily_ops", "delivery_sla", "inventory_exception", "store_performance", "revenue_analysis"]

@router.get("/export")
def export_report(
    report_type: str = Query(..., description="Report category"),
    format: str = Query("csv", description="Format: csv or excel"),
    store_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if report_type not in VALID_REPORTS:
        raise HTTPException(status_code=400, detail=f"Invalid report type. Must be one of: {', '.join(VALID_REPORTS)}")
    
    fmt = format.lower()
    if fmt not in ["csv", "excel"]:
        raise HTTPException(status_code=400, detail="Invalid format. Supported formats: csv, excel")

    file_bytes, media_type, filename = export_report_to_bytes(report_type, fmt, db, store_id=store_id)

    return Response(
        content=file_bytes,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
