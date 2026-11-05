import os
from typing import Dict, Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import Order, Product, DarkStore, DeliveryPartner, Customer, Inventory, Cancellation
from app.schemas.reports import DataQualityReport
from app.services.ingestion_service import process_csv_upload

router = APIRouter(prefix="/data-management", tags=["Data Management"])

@router.post("/upload", response_model=Dict[str, Any])
async def upload_csv_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    
    contents = await file.read()
    report, meta = process_csv_upload(contents, db)

    return {
        "filename": file.filename,
        "metadata": meta,
        "quality_report": report.model_dump()
    }

@router.get("/summary", response_model=Dict[str, Any])
def read_data_summary(db: Session = Depends(get_db)):
    return {
        "total_orders": db.query(Order).count(),
        "total_products": db.query(Product).count(),
        "total_stores": db.query(DarkStore).count(),
        "total_partners": db.query(DeliveryPartner).count(),
        "total_customers": db.query(Customer).count(),
        "total_inventory_records": db.query(Inventory).count(),
        "total_cancellations": db.query(Cancellation).count(),
        "data_sources": {
            "public_benchmark": db.query(Product).filter(Product.data_source == "public_benchmark").count(),
            "synthetic_operational": db.query(Order).filter(Order.data_source == "synthetic_operational").count(),
            "csv_uploaded": db.query(Order).filter(Order.data_source == "csv_upload_ingestion").count()
        }
    }

@router.get("/sample-download")
def download_sample_csv():
    sample_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
        "data", "raw", "sample_orders_upload.csv"
    )
    if os.path.exists(sample_path):
        return FileResponse(
            sample_path,
            filename="sample_orders_template.csv",
            media_type="text/csv"
        )
    raise HTTPException(status_code=404, detail="Sample CSV not found.")
