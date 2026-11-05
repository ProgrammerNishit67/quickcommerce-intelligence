from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.analytics import OperationalAlert
from app.services.alert_service import detect_operational_alerts

router = APIRouter(prefix="/alerts", tags=["Operational Alerts"])

@router.get("", response_model=List[OperationalAlert])
def read_alerts(db: Session = Depends(get_db)):
    return detect_operational_alerts(db)
