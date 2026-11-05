import io
from datetime import datetime
from typing import Dict, Any, Tuple
import pandas as pd
from sqlalchemy.orm import Session
from app.models.entities import Order, DarkStore, Customer
from app.schemas.reports import DataQualityReport

REQUIRED_ORDER_COLUMNS = [
    "order_id", "customer_id", "store_id", "order_timestamp",
    "delivery_status", "total_amount", "net_amount"
]

def process_csv_upload(file_contents: bytes, db: Session) -> Tuple[DataQualityReport, Dict[str, Any]]:
    issues_summary = []
    
    # 1. Read CSV
    try:
        df = pd.read_csv(io.BytesIO(file_contents))
    except Exception as e:
        return DataQualityReport(
            total_records=0,
            valid_records=0,
            missing_values_count=0,
            duplicates_detected=0,
            anomalies_detected=1,
            data_quality_score=0.0,
            issues_summary=[f"Failed to parse CSV file: {str(e)}"]
        ), {"status": "error", "message": "Malformed CSV file format"}

    total_records = len(df)
    if total_records == 0:
        return DataQualityReport(
            total_records=0,
            valid_records=0,
            missing_values_count=0,
            duplicates_detected=0,
            anomalies_detected=0,
            data_quality_score=100.0,
            issues_summary=["Uploaded CSV contains zero records."]
        ), {"status": "empty", "message": "Empty file"}

    # 2. Check Required Columns
    missing_cols = [col for col in REQUIRED_ORDER_COLUMNS if col not in df.columns]
    if missing_cols:
        issues_summary.append(f"Missing mandatory schema columns: {', '.join(missing_cols)}")
        return DataQualityReport(
            total_records=total_records,
            valid_records=0,
            missing_values_count=0,
            duplicates_detected=0,
            anomalies_detected=len(missing_cols),
            data_quality_score=0.0,
            issues_summary=issues_summary
        ), {"status": "error", "message": "Schema mismatch"}

    # 3. Duplicate Detection
    duplicate_mask = df.duplicated(subset=["order_id"], keep="first")
    duplicates_detected = int(duplicate_mask.sum())
    if duplicates_detected > 0:
        issues_summary.append(f"Detected {duplicates_detected} duplicate order_id records (deduplicated automatically).")
        df = df[~duplicate_mask].copy()

    # 4. Missing Values Detection & Cleaning
    missing_values_count = int(df.isnull().sum().sum())
    if missing_values_count > 0:
        issues_summary.append(f"Detected {missing_values_count} missing field entries across dataset.")
    
    # Cleaning & Imputation
    df["discount_amount"] = pd.to_numeric(df.get("discount_amount", 0.0), errors="coerce").fillna(0.0)
    df["delivery_fee"] = pd.to_numeric(df.get("delivery_fee", 15.0), errors="coerce").fillna(15.0)
    df["tip"] = pd.to_numeric(df.get("tip", 0.0), errors="coerce").fillna(0.0)
    df["promised_sla_minutes"] = pd.to_numeric(df.get("promised_sla_minutes", 15), errors="coerce").fillna(15).astype(int)
    df["payment_mode"] = df.get("payment_mode", "UPI").fillna("UPI").astype(str).str.strip()
    df["delivery_status"] = df["delivery_status"].fillna("DELIVERED").astype(str).str.strip()

    # Anomaly checks
    anomalies_detected = 0
    # Negative amount anomaly
    negative_amounts = (df["total_amount"] < 0) | (df["net_amount"] < 0)
    if negative_amounts.any():
        anomalies_detected += int(negative_amounts.sum())
        issues_summary.append(f"Cleaned {int(negative_amounts.sum())} records with negative currency amounts.")
        df = df[~negative_amounts]

    # Calculate Data Quality Score (0-100)
    deductions = (duplicates_detected * 2.0) + (missing_values_count * 0.5) + (anomalies_detected * 5.0)
    data_quality_score = max(0.0, min(100.0, round(100.0 - (deductions / (total_records or 1)), 1)))

    # Ingestion into DB
    ingested_count = 0
    existing_store_ids = set(s[0] for s in db.query(DarkStore.store_id).all())
    existing_cust_ids = set(c[0] for c in db.query(Customer.customer_id).all())

    # Ensure foreign keys or fallback
    for _, row in df.iterrows():
        order_id = str(row["order_id"]).strip()
        cust_id = str(row["customer_id"]).strip()
        store_id = str(row["store_id"]).strip()

        # If foreign keys don't exist in seed, skip or handle safely
        if store_id not in existing_store_ids or cust_id not in existing_cust_ids:
            continue

        existing_order = db.query(Order).filter(Order.order_id == order_id).first()
        if existing_order:
            continue

        try:
            ot = datetime.strptime(str(row["order_timestamp"])[:19], "%Y-%m-%d %H:%M:%S")
        except Exception:
            ot = datetime.now()

        order_obj = Order(
            order_id=order_id,
            customer_id=cust_id,
            store_id=store_id,
            partner_id=str(row.get("partner_id")) if pd.notnull(row.get("partner_id")) else None,
            order_timestamp=ot,
            promised_sla_minutes=int(row["promised_sla_minutes"]),
            delivery_status=str(row["delivery_status"]),
            total_amount=float(row["total_amount"]),
            discount_amount=float(row["discount_amount"]),
            delivery_fee=float(row["delivery_fee"]),
            tip=float(row["tip"]),
            net_amount=float(row["net_amount"]),
            payment_mode=str(row["payment_mode"]),
            delivery_time_minutes=float(row["delivery_time_minutes"]) if pd.notnull(row.get("delivery_time_minutes")) else None,
            is_sla_breached=bool(row.get("is_sla_breached", False)),
            data_source="csv_upload_ingestion"
        )
        db.add(order_obj)
        ingested_count += 1

    db.commit()

    report = DataQualityReport(
        total_records=total_records,
        valid_records=len(df),
        missing_values_count=missing_values_count,
        duplicates_detected=duplicates_detected,
        anomalies_detected=anomalies_detected,
        data_quality_score=data_quality_score,
        issues_summary=issues_summary or ["Dataset passed all validation rules with zero structural anomalies."]
    )

    metadata = {
        "status": "success",
        "ingested_records": ingested_count,
        "processed_rows": len(df),
        "timestamp": datetime.now().isoformat()
    }

    return report, metadata
