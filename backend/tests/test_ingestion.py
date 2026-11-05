import pytest
from app.database import SessionLocal
from app.services.ingestion_service import process_csv_upload

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_csv_upload_validation_and_deduplication(db_session):
    # Sample CSV with valid rows + 1 duplicate order_id
    sample_csv = """order_id,customer_id,store_id,order_timestamp,promised_sla_minutes,delivery_status,total_amount,discount_amount,delivery_fee,tip,net_amount,payment_mode,delivery_time_minutes,is_sla_breached
ORD-TEST-001,CUST-00001,DS-BLR-01,2026-03-01 10:00:00,15,DELIVERED,250.0,0.0,15.0,0.0,265.0,UPI,12.5,0
ORD-TEST-001,CUST-00001,DS-BLR-01,2026-03-01 10:00:00,15,DELIVERED,250.0,0.0,15.0,0.0,265.0,UPI,12.5,0
ORD-TEST-002,CUST-00002,DS-BLR-02,2026-03-01 11:30:00,15,CANCELLED,180.0,0.0,15.0,0.0,195.0,UPI,,1
""".encode("utf-8")

    report, meta = process_csv_upload(sample_csv, db_session)

    assert report.total_records == 3
    assert report.duplicates_detected == 1
    assert report.valid_records == 2
    assert report.data_quality_score >= 80.0
    assert meta["status"] == "success"

def test_csv_upload_missing_schema(db_session):
    # Missing required order_id and store_id
    malformed_csv = """customer_id,order_timestamp,total_amount
CUST-00001,2026-03-01 10:00:00,250.0
""".encode("utf-8")

    report, meta = process_csv_upload(malformed_csv, db_session)
    assert report.valid_records == 0
    assert meta["status"] == "error"
    assert report.data_quality_score == 0.0
