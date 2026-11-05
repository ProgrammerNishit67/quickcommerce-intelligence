from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.database import get_db
from app.models.entities import DarkStore, Order, Inventory
from app.services.analytics_service import apply_order_filters

router = APIRouter(prefix="/store-performance", tags=["Store Performance"])

@router.get("", response_model=List[Dict[str, Any]])
def read_store_performance_rankings(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    stores = db.query(DarkStore).all()
    results = []

    for s in stores:
        ord_q = db.query(Order).filter(Order.store_id == s.store_id)
        ord_q = apply_order_filters(ord_q, start_date, end_date)
        total_orders = ord_q.count()
        deliv_orders = ord_q.filter(Order.delivery_status == "DELIVERED").count()
        cancelled_orders = ord_q.filter(Order.delivery_status == "CANCELLED").count()
        
        net_revenue = ord_q.filter(Order.delivery_status == "DELIVERED").with_entities(func.sum(Order.net_amount)).scalar() or 0.0
        avg_time = ord_q.filter(Order.delivery_status == "DELIVERED").with_entities(func.avg(Order.delivery_time_minutes)).scalar() or 0.0
        on_time_count = ord_q.filter(Order.delivery_status == "DELIVERED", Order.is_sla_breached == False).count()

        sla_pct = round((on_time_count * 100.0 / deliv_orders), 1) if deliv_orders > 0 else 0.0
        cncl_pct = round((cancelled_orders * 100.0 / total_orders), 1) if total_orders > 0 else 0.0
        aov = round(net_revenue / deliv_orders, 2) if deliv_orders > 0 else 0.0

        # Inventory in-stock
        total_inv = db.query(Inventory).filter(Inventory.store_id == s.store_id).count() or 1
        stockout_inv = db.query(Inventory).filter(Inventory.store_id == s.store_id, Inventory.stockout_flag == True).count()
        in_stock_pct = round(((total_inv - stockout_inv) * 100.0 / total_inv), 1)

        # Composite score out of 100
        # 35% revenue normalized + 30% SLA + 20% low cancel + 15% inventory
        composite_score = round(
            min(35.0, (net_revenue / 4000.0) * 35.0) +
            (sla_pct * 0.30) +
            ((100.0 - cncl_pct) * 0.20) +
            (in_stock_pct * 0.15), 1
        )

        results.append({
            "store_id": s.store_id,
            "store_name": s.store_name,
            "city": s.city,
            "locality": s.locality,
            "riders_allocated": s.active_riders_allocated,
            "capacity_per_hour": s.capacity_orders_per_hour,
            "total_orders": total_orders,
            "delivered_orders": deliv_orders,
            "net_revenue": round(float(net_revenue), 2),
            "aov": aov,
            "avg_delivery_time": round(float(avg_time), 1),
            "sla_adherence_pct": sla_pct,
            "cancellation_rate_pct": cncl_pct,
            "in_stock_rate_pct": in_stock_pct,
            "composite_score": composite_score
        })

    results.sort(key=lambda x: x["composite_score"], reverse=True)
    # Add rank
    for rank, item in enumerate(results, start=1):
        item["national_rank"] = rank

    return results
