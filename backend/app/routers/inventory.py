from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.analytics import InventoryIntelligenceResponse
from app.services.analytics_service import get_inventory_data

router = APIRouter(prefix="/inventory", tags=["Inventory Intelligence"])

@router.get("", response_model=InventoryIntelligenceResponse)
def read_inventory_intelligence(
    store_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_inventory_data(db, store_id=store_id, category=category)
