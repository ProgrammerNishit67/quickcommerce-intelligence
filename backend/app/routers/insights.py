from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.analytics import BusinessInsight
from app.services.insight_service import generate_business_insights

router = APIRouter(prefix="/insights", tags=["Business Insights"])

@router.get("", response_model=List[BusinessInsight])
def read_business_insights(db: Session = Depends(get_db)):
    return generate_business_insights(db)
