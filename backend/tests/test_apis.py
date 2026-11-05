import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_metadata_filters_endpoint():
    res = client.get("/api/metadata/filters")
    assert res.status_code == 200
    data = res.json()
    assert "stores" in data
    assert "categories" in data
    assert len(data["stores"]) > 0
    assert len(data["categories"]) > 0

def test_overview_endpoint():
    res = client.get("/api/overview")
    assert res.status_code == 200
    data = res.json()
    assert "kpis" in data
    assert "daily_trends" in data
    assert "store_performance" in data
    assert "category_performance" in data
    assert data["kpis"]["total_orders"] > 0
    assert data["kpis"]["net_revenue"] > 0

def test_delivery_endpoint():
    res = client.get("/api/delivery")
    assert res.status_code == 200
    data = res.json()
    assert "avg_delivery_time" in data
    assert "on_time_rate" in data
    assert "hourly_trends" in data
    assert len(data["hourly_trends"]) > 0

def test_inventory_endpoint():
    res = client.get("/api/inventory")
    assert res.status_code == 200
    data = res.json()
    assert "total_skus" in data
    assert "replenishment_recommendations" in data

def test_revenue_endpoint():
    res = client.get("/api/revenue")
    assert res.status_code == 200
    data = res.json()
    assert "total_gmv" in data
    assert "payment_mode_split" in data

def test_order_quality_endpoint():
    res = client.get("/api/order-quality")
    assert res.status_code == 200
    data = res.json()
    assert "total_cancellations" in data
    assert "cancellation_reasons" in data

def test_store_performance_endpoint():
    res = client.get("/api/store-performance")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "composite_score" in data[0]

def test_alerts_endpoint():
    res = client.get("/api/alerts")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)

def test_insights_endpoint():
    res = client.get("/api/insights")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_reports_export_csv():
    res = client.get("/api/reports/export?report_type=daily_ops&format=csv")
    assert res.status_code == 200
    assert "text/csv" in res.headers["content-type"]
    assert len(res.content) > 50

def test_reports_export_excel():
    res = client.get("/api/reports/export?report_type=delivery_sla&format=excel")
    assert res.status_code == 200
    assert "spreadsheetml" in res.headers["content-type"]
    assert len(res.content) > 100
