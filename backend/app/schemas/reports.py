from typing import List, Optional
from pydantic import BaseModel

class ReportExportRequest(BaseModel):
    report_type: str # daily_ops, delivery_sla, inventory_exception, store_performance, revenue_analysis
    format: str = "csv" # csv or excel
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    store_id: Optional[str] = None

class DataQualityReport(BaseModel):
    total_records: int
    valid_records: int
    missing_values_count: int
    duplicates_detected: int
    anomalies_detected: int
    data_quality_score: float
    issues_summary: List[str]
