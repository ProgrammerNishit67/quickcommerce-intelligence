import pytest
from app.database import SessionLocal
from app.models.entities import Order, DarkStore, Product, Inventory, Cancellation
from app.services.analytics_service import get_overview_data, get_delivery_data, get_inventory_data

@pytest.fixture(scope="module")
def db_session():
    db = SessionLocal()
    yield db
    db.close()

def test_kpi_no_revenue_double_counting(db_session):
    """
    Ensure that cancelled orders are NOT double counted in Net Revenue.
    Net Revenue must strictly equal the sum of net_amount for DELIVERED orders only.
    """
    overview = get_overview_data(db_session)
    
    # Calculate directly from DB
    delivered_orders = db_session.query(Order).filter(Order.delivery_status == "DELIVERED").all()
    expected_net_revenue = round(sum(o.net_amount for o in delivered_orders), 2)
    
    assert overview.kpis.net_revenue == expected_net_revenue
    assert overview.kpis.net_revenue <= overview.kpis.total_gmv

def test_aov_calculation_accuracy(db_session):
    """
    AOV must equal Net Revenue divided by Delivered Orders (not total orders including cancelled).
    """
    overview = get_overview_data(db_session)
    delivered_count = db_session.query(Order).filter(Order.delivery_status == "DELIVERED").count()
    expected_aov = round(overview.kpis.net_revenue / delivered_count, 2)
    
    assert abs(overview.kpis.average_order_value - expected_aov) < 0.05

def test_delivery_sla_percentage(db_session):
    """
    On-Time Delivery Rate + SLA Breach Rate must sum to 100%.
    """
    delivery = get_delivery_data(db_session)
    assert abs((delivery.on_time_rate + delivery.sla_breach_rate) - 100.0) < 0.2

def test_inventory_reconciliation(db_session):
    """
    Stockout rate must reconcile with current_stock == 0 and total inventory records.
    """
    inv = get_inventory_data(db_session)
    total_inv = db_session.query(Inventory).count()
    zero_stock_inv = db_session.query(Inventory).filter(Inventory.current_stock == 0).count()
    expected_stockout_rate = round((zero_stock_inv * 100.0 / total_inv), 1)
    
    assert inv.total_skus == total_inv
    assert inv.stockout_count == zero_stock_inv
    assert abs(inv.stockout_rate - expected_stockout_rate) < 0.2

def test_cancellation_denominator(db_session):
    """
    Cancellation rate denominator must be Total Orders (all placed orders).
    """
    overview = get_overview_data(db_session)
    total_orders = db_session.query(Order).count()
    cancelled_orders = db_session.query(Order).filter(Order.delivery_status == "CANCELLED").count()
    expected_cancellation_rate = round((cancelled_orders * 100.0 / total_orders), 1)
    
    assert abs(overview.kpis.cancellation_rate - expected_cancellation_rate) < 0.2
