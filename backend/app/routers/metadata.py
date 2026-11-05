from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.entities import DarkStore, Product

router = APIRouter(prefix="/metadata", tags=["Metadata"])

@router.get("/filters", response_model=Dict[str, Any])
def read_filter_metadata(db: Session = Depends(get_db)):
    stores = db.query(DarkStore.store_id, DarkStore.store_name, DarkStore.city).order_by(DarkStore.city, DarkStore.store_name).all()
    categories = db.query(Product.category).distinct().order_by(Product.category).all()

    return {
        "stores": [{"store_id": s[0], "store_name": s[1], "city": s[2]} for s in stores],
        "categories": [c[0] for c in categories]
    }
