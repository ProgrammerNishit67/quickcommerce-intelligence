from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models.entities import DarkStore, Order, Inventory
from app.schemas.analytics import OperationalAlert

def detect_operational_alerts(db: Session) -> List[OperationalAlert]:
    alerts: List[OperationalAlert] = []
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Unusual Delivery Time / SLA Breaches by Store
    store_deliv = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        func.count(Order.order_id).label("total_orders"),
        func.avg(Order.delivery_time_minutes).label("avg_time"),
        func.sum(case((Order.is_sla_breached == True, 1), else_=0)).label("breaches")
    ).join(Order, DarkStore.store_id == Order.store_id)\
     .filter(Order.delivery_status == "DELIVERED")\
     .group_by(DarkStore.store_id, DarkStore.store_name).all()

    for s in store_deliv:
        tot = s.total_orders or 1
        avg_t = float(s.avg_time or 0.0)
        breach_pct = (s.breaches * 100.0 / tot)

        if avg_t > 16.0 or breach_pct > 15.0:
            alerts.append(OperationalAlert(
                id=f"ALT-DELIV-{s.store_id}",
                title=f"Delivery SLA Breach Surge: {s.store_name}",
                category="DELIVERY",
                severity="CRITICAL" if avg_t > 17.5 or breach_pct > 20.0 else "WARNING",
                store_name=s.store_name,
                metric_value=f"Avg {avg_t:.1f} mins ({breach_pct:.1f}% breach)",
                threshold="< 15.0 mins (SLA breach < 10%)",
                detected_at=now_str,
                description=f"Store '{s.store_name}' is violating promised 15-minute quick commerce SLAs with {s.breaches} delayed dispatches.",
                recommended_action="Reallocate 4-6 reserve EV riders from neighboring pods and expedite order bagging buffer."
            ))

    # 2. Cancellation Spike Detection
    store_cncl = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        func.count(Order.order_id).label("total_orders"),
        func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("cancellations")
    ).join(Order, DarkStore.store_id == Order.store_id)\
     .group_by(DarkStore.store_id, DarkStore.store_name).all()

    for c in store_cncl:
        tot = c.total_orders or 1
        cn = c.cancellations or 0
        rate = (cn * 100.0 / tot)
        if rate > 5.0:
            alerts.append(OperationalAlert(
                id=f"ALT-CNCL-{c.store_id}",
                title=f"Elevated Order Cancellation Rate: {c.store_name}",
                category="CANCELLATION",
                severity="CRITICAL" if rate > 6.5 else "WARNING",
                store_name=c.store_name,
                metric_value=f"{rate:.1f}% Cancellation Rate ({cn} orders)",
                threshold="< 4.0% industry standard",
                detected_at=now_str,
                description=f"Elevated cancellation volume observed at {c.store_name}. Top drivers include delivery overshoot and stock unavailability.",
                recommended_action="Initiate immediate review with Dark Store Hub Manager and reconcile real-time physical shelf counts."
            ))

    # 3. High Inventory Stockout Rates
    store_inv = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        func.count(Inventory.inventory_id).label("total_skus"),
        func.sum(case((Inventory.stockout_flag == True, 1), else_=0)).label("stockouts"),
        func.sum(case((Inventory.current_stock == 0, 1), else_=0)).label("zero_stock")
    ).join(Inventory, DarkStore.store_id == Inventory.store_id)\
     .group_by(DarkStore.store_id, DarkStore.store_name).all()

    for inv in store_inv:
        tot = inv.total_skus or 1
        so = inv.stockouts or 0
        rate = (so * 100.0 / tot)
        if rate > 8.0:
            alerts.append(OperationalAlert(
                id=f"ALT-STK-{inv.store_id}",
                title=f"Critical Inventory Stockout Rate: {inv.store_name}",
                category="INVENTORY",
                severity="CRITICAL" if rate > 12.0 else "WARNING",
                store_name=inv.store_name,
                metric_value=f"{rate:.1f}% SKUs at Risk ({so} SKUs below safety stock)",
                threshold="< 5.0% threshold",
                detected_at=now_str,
                description=f"Persistent stockouts detected across high-velocity FMCG items at {inv.store_name}, causing customer basket dropoffs.",
                recommended_action="Dispatch immediate inter-store inventory transfer from central fulfillment mother hub."
            ))

    # 4. Underperforming Store / Low Ticket Size
    for s in store_deliv:
        rev_q = db.query(func.sum(Order.net_amount))\
                  .filter(Order.store_id == s.store_id, Order.delivery_status == "DELIVERED").scalar() or 0.0
        avg_basket = rev_q / (s.total_orders or 1)
        if avg_basket < 260.0:
            alerts.append(OperationalAlert(
                id=f"ALT-REV-{s.store_id}",
                title=f"Sub-Optimal Basket Size (AOV Leakage): {s.store_name}",
                category="REVENUE",
                severity="INFO",
                store_name=s.store_name,
                metric_value=f"₹{avg_basket:.1f} Average Order Value",
                threshold="> ₹300.00 target AOV",
                detected_at=now_str,
                description=f"Customers in {s.store_name} catchment area are placing low-ticket transactions with high delivery subsidy cost.",
                recommended_action="Implement smart cart bundling (e.g. Free delivery threshold at ₹299, Snack + Drink cross-sell at checkout)."
            ))

    return alerts
