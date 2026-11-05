from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.analytics import RevenueAnalyticsResponse
from app.services.analytics_service import get_revenue_data

router = APIRouter(prefix="/revenue", tags=["Revenue Analytics"])

@router.get("", response_model=RevenueAnalyticsResponse)
def read_revenue_analytics(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    store_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_revenue_data(db, start_date=start_date, end_date=end_date, store_id=store_id)
