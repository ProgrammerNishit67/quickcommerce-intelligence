from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc, text
from app.models.entities import (
    DarkStore,
    Product,
    Customer,
    DeliveryPartner,
    Order,
    OrderItem,
    Inventory,
    Promotion,
    Cancellation
)
from app.schemas.analytics import (
    OverviewKPIs,
    TrendPoint,
    StoreBreakdown,
    CategoryBreakdown,
    OverviewResponse,
    DeliveryAnalyticsResponse,
    InventoryIntelligenceResponse,
    RevenueAnalyticsResponse,
    OrderQualityResponse
)

def apply_order_filters(query, start_date: Optional[str] = None, end_date: Optional[str] = None, store_id: Optional[str] = None):
    if start_date:
        query = query.filter(Order.order_timestamp >= f"{start_date} 00:00:00")
    if end_date:
        query = query.filter(Order.order_timestamp <= f"{end_date} 23:59:59")
    if store_id and store_id != "all":
        query = query.filter(Order.store_id == store_id)
    return query

def get_overview_data(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None, store_id: Optional[str] = None) -> OverviewResponse:
    base_q = db.query(Order)
    base_q = apply_order_filters(base_q, start_date, end_date, store_id)

    total_orders = base_q.count()
    delivered_orders = base_q.filter(Order.delivery_status == "DELIVERED").count()
    cancelled_orders = base_q.filter(Order.delivery_status == "CANCELLED").count()

    total_gmv = base_q.with_entities(func.sum(Order.total_amount)).scalar() or 0.0
    net_revenue = base_q.filter(Order.delivery_status == "DELIVERED").with_entities(func.sum(Order.net_amount)).scalar() or 0.0
    
    aov = (net_revenue / delivered_orders) if delivered_orders > 0 else 0.0

    avg_delivery_time = base_q.filter(Order.delivery_status == "DELIVERED", Order.delivery_time_minutes.isnot(None))\
                              .with_entities(func.avg(Order.delivery_time_minutes)).scalar() or 0.0

    on_time_count = base_q.filter(Order.delivery_status == "DELIVERED", Order.is_sla_breached == False).count()
    on_time_rate = (on_time_count * 100.0 / delivered_orders) if delivered_orders > 0 else 0.0
    cancellation_rate = (cancelled_orders * 100.0 / total_orders) if total_orders > 0 else 0.0

    active_stores = db.query(DarkStore).filter(DarkStore.status == "ACTIVE").count()

    kpis = OverviewKPIs(
        total_orders=total_orders,
        total_gmv=round(float(total_gmv), 2),
        net_revenue=round(float(net_revenue), 2),
        average_order_value=round(float(aov), 2),
        average_delivery_time=round(float(avg_delivery_time), 1),
        on_time_delivery_rate=round(float(on_time_rate), 1),
        cancellation_rate=round(float(cancellation_rate), 1),
        active_stores=active_stores
    )

    # Daily trends (date group)
    trend_q = db.query(
        func.date(Order.order_timestamp).label("order_date"),
        func.count(Order.order_id).label("orders"),
        func.sum(case((Order.delivery_status == "DELIVERED", Order.net_amount), else_=0.0)).label("revenue"),
        func.sum(case((Order.delivery_status == "DELIVERED", 1), else_=0)).label("delivered_count"),
        func.sum(case((Order.delivery_status == "DELIVERED", case((Order.is_sla_breached == False, 1), else_=0)), else_=0)).label("on_time_count"),
        func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("cancellations")
    )
    trend_q = apply_order_filters(trend_q, start_date, end_date, store_id)
    trend_rows = trend_q.group_by("order_date").order_by("order_date").all()

    daily_trends = []
    for r in trend_rows:
        deliv = r.delivered_count or 0
        rev = float(r.revenue or 0.0)
        daily_aov = round(rev / deliv, 2) if deliv > 0 else 0.0
        on_time = round((r.on_time_count * 100.0 / deliv), 1) if deliv > 0 else 0.0
        daily_trends.append(TrendPoint(
            date=str(r.order_date),
            orders=int(r.orders),
            revenue=round(rev, 2),
            aov=daily_aov,
            on_time_rate=on_time,
            cancellations=int(r.cancellations or 0)
        ))

    # Store Breakdown
    store_q = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        DarkStore.city,
        func.count(Order.order_id).label("orders"),
        func.sum(case((Order.delivery_status == "DELIVERED", Order.net_amount), else_=0.0)).label("revenue"),
        func.avg(case((Order.delivery_status == "DELIVERED", Order.delivery_time_minutes), else_=None)).label("avg_time"),
        func.sum(case((Order.delivery_status == "DELIVERED", 1), else_=0)).label("delivered_count"),
        func.sum(case((Order.delivery_status == "DELIVERED", case((Order.is_sla_breached == False, 1), else_=0)), else_=0)).label("on_time_count"),
        func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("cancellations")
    ).join(Order, DarkStore.store_id == Order.store_id)
    store_q = apply_order_filters(store_q, start_date, end_date, store_id)
    store_rows = store_q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city).all()

    store_performance = []
    for s in store_rows:
        deliv = s.delivered_count or 0
        tot = s.orders or 0
        on_time = round((s.on_time_count * 100.0 / deliv), 1) if deliv > 0 else 0.0
        cncl_rate = round((s.cancellations * 100.0 / tot), 1) if tot > 0 else 0.0
        store_performance.append(StoreBreakdown(
            store_id=s.store_id,
            store_name=s.store_name,
            city=s.city,
            orders=int(tot),
            revenue=round(float(s.revenue or 0.0), 2),
            avg_delivery_time=round(float(s.avg_time or 0.0), 1),
            on_time_rate=on_time,
            cancellation_rate=cncl_rate
        ))
    store_performance.sort(key=lambda x: x.revenue, reverse=True)

    # Category performance
    cat_q = db.query(
        Product.category,
        func.sum(OrderItem.quantity).label("units_sold"),
        func.sum(OrderItem.total_price).label("sales_val"),
        func.sum(OrderItem.quantity * Product.cost_price).label("cogs")
    ).join(OrderItem, Product.sku_id == OrderItem.sku_id)\
     .join(Order, OrderItem.order_id == Order.order_id)
    cat_q = apply_order_filters(cat_q, start_date, end_date, store_id)
    cat_rows = cat_q.filter(Order.delivery_status == "DELIVERED").group_by(Product.category).all()

    total_cat_rev = sum(float(c.sales_val or 0.0) for c in cat_rows) or 1.0
    category_performance = []
    for c in cat_rows:
        sales = float(c.sales_val or 0.0)
        cogs = float(c.cogs or 0.0)
        profit = sales - cogs
        margin_pct = round((profit * 100.0 / sales), 1) if sales > 0 else 0.0
        share_pct = round((sales * 100.0 / total_cat_rev), 1)
        category_performance.append(CategoryBreakdown(
            category=c.category,
            units_sold=int(c.units_sold or 0),
            revenue=round(sales, 2),
            gross_margin_pct=margin_pct,
            share_pct=share_pct
        ))
    category_performance.sort(key=lambda x: x.revenue, reverse=True)

    return OverviewResponse(
        kpis=kpis,
        daily_trends=daily_trends,
        store_performance=store_performance,
        category_performance=category_performance
    )

def get_delivery_data(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None, store_id: Optional[str] = None) -> DeliveryAnalyticsResponse:
    base_q = db.query(Order).filter(Order.delivery_status == "DELIVERED")
    base_q = apply_order_filters(base_q, start_date, end_date, store_id)

    total_deliv = base_q.count()
    avg_delivery_time = base_q.with_entities(func.avg(Order.delivery_time_minutes)).scalar() or 0.0
    breaches = base_q.filter(Order.is_sla_breached == True).count()
    breach_rate = (breaches * 100.0 / total_deliv) if total_deliv > 0 else 0.0
    on_time_rate = 100.0 - breach_rate

    # Hourly distribution
    hourly_q = db.query(
        func.strftime("%H", Order.order_timestamp).label("hour"),
        func.count(Order.order_id).label("order_count"),
        func.avg(Order.delivery_time_minutes).label("avg_time"),
        func.sum(case((Order.is_sla_breached == True, 1), else_=0)).label("breach_count")
    ).filter(Order.delivery_status == "DELIVERED")
    hourly_q = apply_order_filters(hourly_q, start_date, end_date, store_id)
    hourly_rows = hourly_q.group_by("hour").order_by("hour").all()

    hourly_trends = []
    for h in hourly_rows:
        tot = h.order_count or 0
        br = h.breach_count or 0
        rate = round((br * 100.0 / tot), 1) if tot > 0 else 0.0
        hourly_trends.append({
            "hour": f"{int(h.hour):02d}:00",
            "orders": tot,
            "avg_time": round(float(h.avg_time or 0.0), 1),
            "breaches": br,
            "breach_rate": rate
        })

    # Store performance
    store_q = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        DarkStore.city,
        DarkStore.active_riders_allocated,
        func.count(Order.order_id).label("total_orders"),
        func.avg(Order.delivery_time_minutes).label("avg_time"),
        func.sum(case((Order.is_sla_breached == True, 1), else_=0)).label("breaches")
    ).join(Order, DarkStore.store_id == Order.store_id)\
     .filter(Order.delivery_status == "DELIVERED")
    store_q = apply_order_filters(store_q, start_date, end_date, store_id)
    store_rows = store_q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city, DarkStore.active_riders_allocated).all()

    store_delivery_performance = []
    for s in store_rows:
        tot = s.total_orders or 0
        br = s.breaches or 0
        on_time = round(((tot - br) * 100.0 / tot), 1) if tot > 0 else 0.0
        store_delivery_performance.append({
            "store_id": s.store_id,
            "store_name": s.store_name,
            "city": s.city,
            "riders": s.active_riders_allocated,
            "total_orders": tot,
            "avg_time": round(float(s.avg_time or 0.0), 1),
            "breaches": br,
            "on_time_rate": on_time
        })
    store_delivery_performance.sort(key=lambda x: x["on_time_rate"], reverse=True)

    # Delay buckets
    delay_buckets = [
        {"tier": "< 10 Mins (Fast)", "min": 0, "max": 10},
        {"tier": "10-15 Mins (Standard)", "min": 10, "max": 15},
        {"tier": "15-20 Mins (Minor Delay)", "min": 15, "max": 20},
        {"tier": "20-25 Mins (Delayed)", "min": 20, "max": 25},
        {"tier": "> 25 Mins (Severe Delay)", "min": 25, "max": 999}
    ]
    delay_breakdown = []
    for b in delay_buckets:
        cnt = base_q.filter(Order.delivery_time_minutes >= b["min"], Order.delivery_time_minutes < b["max"]).count()
        delay_breakdown.append({
            "tier": b["tier"],
            "orders": cnt,
            "percentage": round((cnt * 100.0 / total_deliv), 1) if total_deliv > 0 else 0.0
        })

    # Partner rankings
    p_q = db.query(
        DeliveryPartner.partner_id,
        DeliveryPartner.name,
        DeliveryPartner.vehicle_type,
        DeliveryPartner.rating,
        func.count(Order.order_id).label("trips"),
        func.avg(Order.delivery_time_minutes).label("avg_time"),
        func.sum(case((Order.is_sla_breached == False, 1), else_=0)).label("on_time_count")
    ).join(Order, DeliveryPartner.partner_id == Order.partner_id)\
     .filter(Order.delivery_status == "DELIVERED")
    p_q = apply_order_filters(p_q, start_date, end_date, store_id)
    p_rows = p_q.group_by(DeliveryPartner.partner_id, DeliveryPartner.name, DeliveryPartner.vehicle_type, DeliveryPartner.rating)\
                .having(func.count(Order.order_id) >= 5).order_by(desc("trips")).limit(15).all()

    partner_performance = []
    for p in p_rows:
        trips = p.trips or 0
        ot = p.on_time_count or 0
        partner_performance.append({
            "partner_id": p.partner_id,
            "name": p.name,
            "vehicle_type": p.vehicle_type,
            "rating": round(float(p.rating), 2),
            "trips": trips,
            "avg_time": round(float(p.avg_time or 0.0), 1),
            "sla_compliance_pct": round((ot * 100.0 / trips), 1) if trips > 0 else 0.0
        })

    return DeliveryAnalyticsResponse(
        avg_delivery_time=round(float(avg_delivery_time), 1),
        on_time_rate=round(float(on_time_rate), 1),
        sla_breaches=breaches,
        sla_breach_rate=round(float(breach_rate), 1),
        hourly_trends=hourly_trends,
        store_delivery_performance=store_delivery_performance,
        delay_breakdown=delay_breakdown,
        partner_performance=partner_performance
    )

def get_inventory_data(db: Session, store_id: Optional[str] = None, category: Optional[str] = None) -> InventoryIntelligenceResponse:
    inv_q = db.query(Inventory).join(Product, Inventory.sku_id == Product.sku_id)
    if store_id and store_id != "all":
        inv_q = inv_q.filter(Inventory.store_id == store_id)
    if category and category != "all":
        inv_q = inv_q.filter(Product.category == category)

    total_skus = inv_q.count()
    stockout_count = inv_q.filter(Inventory.current_stock == 0).count()
    low_stock_count = inv_q.filter(Inventory.current_stock <= Inventory.safety_stock, Inventory.current_stock > 0).count()
    stockout_rate = round((stockout_count * 100.0 / total_skus), 1) if total_skus > 0 else 0.0

    # Category inventory breakdown
    cat_inv_q = db.query(
        Product.category,
        func.count(Inventory.inventory_id).label("item_count"),
        func.sum(Inventory.current_stock).label("units_in_stock"),
        func.sum(case((Inventory.current_stock <= Inventory.safety_stock, 1), else_=0)).label("critical_items"),
        func.sum(Inventory.current_stock * Product.cost_price).label("holding_value")
    ).join(Inventory, Product.sku_id == Inventory.sku_id)
    if store_id and store_id != "all":
        cat_inv_q = cat_inv_q.filter(Inventory.store_id == store_id)
    cat_inv_rows = cat_inv_q.group_by(Product.category).all()

    category_inventory = []
    total_holding = 0.0
    for c in cat_inv_rows:
        val = float(c.holding_value or 0.0)
        total_holding += val
        category_inventory.append({
            "category": c.category,
            "items_count": int(c.item_count),
            "units_in_stock": int(c.units_in_stock or 0),
            "critical_items": int(c.critical_items or 0),
            "holding_value": round(val, 2)
        })

    # Fast-moving products (top units sold)
    sales_q = db.query(
        Product.sku_id,
        Product.name,
        Product.category,
        Product.mrp,
        Product.cost_price,
        func.sum(OrderItem.quantity).label("units_sold"),
        func.sum(OrderItem.total_price).label("revenue")
    ).join(OrderItem, Product.sku_id == OrderItem.sku_id)\
     .join(Order, OrderItem.order_id == Order.order_id)\
     .filter(Order.delivery_status == "DELIVERED")
    if store_id and store_id != "all":
        sales_q = sales_q.filter(Order.store_id == store_id)
    if category and category != "all":
        sales_q = sales_q.filter(Product.category == category)
    
    top_sales = sales_q.group_by(Product.sku_id, Product.name, Product.category, Product.mrp, Product.cost_price)\
                       .order_by(desc("units_sold")).all()

    fast_moving = []
    for p in top_sales[:10]:
        fast_moving.append({
            "sku_id": p.sku_id,
            "name": p.name,
            "category": p.category,
            "mrp": float(p.mrp),
            "units_sold": int(p.units_sold or 0),
            "revenue": round(float(p.revenue or 0.0), 2)
        })

    slow_moving = []
    for p in reversed(top_sales[-10:]):
        slow_moving.append({
            "sku_id": p.sku_id,
            "name": p.name,
            "category": p.category,
            "mrp": float(p.mrp),
            "units_sold": int(p.units_sold or 0),
            "revenue": round(float(p.revenue or 0.0), 2)
        })

    # Replenishment recommendations
    replenish_q = db.query(
        DarkStore.store_name,
        Product.sku_id,
        Product.name,
        Product.category,
        Product.cost_price,
        Inventory.current_stock,
        Inventory.safety_stock,
        Inventory.reorder_level
    ).join(DarkStore, Inventory.store_id == DarkStore.store_id)\
     .join(Product, Inventory.sku_id == Product.sku_id)\
     .filter(Inventory.current_stock <= Inventory.reorder_level)
    if store_id and store_id != "all":
        replenish_q = replenish_q.filter(Inventory.store_id == store_id)
    if category and category != "all":
        replenish_q = replenish_q.filter(Product.category == category)
    
    replenish_rows = replenish_q.order_by(Inventory.current_stock.asc()).limit(20).all()
    replenish_recs = []
    for r in replenish_rows:
        suggested = int((r.reorder_level * 2.5) - r.current_stock)
        cost = round(suggested * float(r.cost_price), 2)
        status = "URGENT_STOCKOUT" if r.current_stock <= r.safety_stock else "REORDER_QUEUE"
        replenish_recs.append({
            "store_name": r.store_name,
            "sku_id": r.sku_id,
            "name": r.name,
            "category": r.category,
            "current_stock": r.current_stock,
            "safety_stock": r.safety_stock,
            "reorder_level": r.reorder_level,
            "suggested_units": suggested,
            "estimated_cost": cost,
            "urgency": status
        })

    total_cogs = sum(p.units_sold * float(p.cost_price) for p in top_sales) or 1.0
    overall_turnover = round((total_cogs / (total_holding or 1.0)), 2)

    return InventoryIntelligenceResponse(
        total_skus=total_skus,
        stockout_count=stockout_count,
        stockout_rate=stockout_rate,
        low_stock_count=low_stock_count,
        overall_turnover_ratio=overall_turnover,
        category_inventory=category_inventory,
        fast_moving_products=fast_moving,
        slow_moving_products=slow_moving,
        replenishment_recommendations=replenish_recs
    )

def get_revenue_data(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None, store_id: Optional[str] = None) -> RevenueAnalyticsResponse:
    base_q = db.query(Order).filter(Order.delivery_status == "DELIVERED")
    base_q = apply_order_filters(base_q, start_date, end_date, store_id)

    total_orders = base_q.count()
    gross_gmv = base_q.with_entities(func.sum(Order.total_amount)).scalar() or 0.0
    net_rev = base_q.with_entities(func.sum(Order.net_amount)).scalar() or 0.0
    total_discounts = base_q.with_entities(func.sum(Order.discount_amount)).scalar() or 0.0
    aov = (net_rev / total_orders) if total_orders > 0 else 0.0
    burn_rate = (total_discounts * 100.0 / (gross_gmv or 1.0))

    # Revenue daily trends
    trend_q = db.query(
        func.date(Order.order_timestamp).label("order_date"),
        func.sum(Order.total_amount).label("gmv"),
        func.sum(Order.net_amount).label("net_revenue"),
        func.sum(Order.discount_amount).label("discounts"),
        func.count(Order.order_id).label("orders")
    ).filter(Order.delivery_status == "DELIVERED")
    trend_q = apply_order_filters(trend_q, start_date, end_date, store_id)
    trend_rows = trend_q.group_by("order_date").order_by("order_date").all()

    revenue_trends = []
    for r in trend_rows:
        cnt = r.orders or 1
        net = float(r.net_revenue or 0.0)
        revenue_trends.append({
            "date": str(r.order_date),
            "gmv": round(float(r.gmv or 0.0), 2),
            "net_revenue": round(net, 2),
            "discounts": round(float(r.discounts or 0.0), 2),
            "aov": round(net / cnt, 2)
        })

    # Category Revenue
    cat_q = db.query(
        Product.category,
        func.sum(OrderItem.total_price).label("revenue"),
        func.sum(OrderItem.quantity).label("units_sold"),
        func.sum(OrderItem.quantity * Product.cost_price).label("cogs")
    ).join(OrderItem, Product.sku_id == OrderItem.sku_id)\
     .join(Order, OrderItem.order_id == Order.order_id)\
     .filter(Order.delivery_status == "DELIVERED")
    cat_q = apply_order_filters(cat_q, start_date, end_date, store_id)
    cat_rows = cat_q.group_by(Product.category).order_by(desc("revenue")).all()

    category_revenue = []
    for c in cat_rows:
        rev = float(c.revenue or 0.0)
        cogs = float(c.cogs or 0.0)
        margin = round(((rev - cogs) * 100.0 / (rev or 1.0)), 1)
        category_revenue.append({
            "category": c.category,
            "revenue": round(rev, 2),
            "units_sold": int(c.units_sold or 0),
            "margin_pct": margin
        })

    # Store Revenue
    s_q = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        DarkStore.city,
        func.count(Order.order_id).label("orders"),
        func.sum(Order.net_amount).label("revenue"),
        func.sum(Order.discount_amount).label("discounts")
    ).join(Order, DarkStore.store_id == Order.store_id)\
     .filter(Order.delivery_status == "DELIVERED")
    s_q = apply_order_filters(s_q, start_date, end_date, store_id)
    s_rows = s_q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city).order_by(desc("revenue")).all()

    store_revenue = []
    for s in s_rows:
        cnt = s.orders or 1
        rev = float(s.revenue or 0.0)
        store_revenue.append({
            "store_id": s.store_id,
            "store_name": s.store_name,
            "city": s.city,
            "orders": cnt,
            "revenue": round(rev, 2),
            "aov": round(rev / cnt, 2),
            "discounts": round(float(s.discounts or 0.0), 2)
        })

    # Payment Mode Split
    pay_q = db.query(
        Order.payment_mode,
        func.count(Order.order_id).label("orders"),
        func.sum(Order.net_amount).label("revenue")
    ).filter(Order.delivery_status == "DELIVERED")
    pay_q = apply_order_filters(pay_q, start_date, end_date, store_id)
    pay_rows = pay_q.group_by(Order.payment_mode).order_by(desc("revenue")).all()

    payment_mode_split = []
    for p in pay_rows:
        payment_mode_split.append({
            "mode": p.payment_mode,
            "orders": int(p.orders),
            "revenue": round(float(p.revenue or 0.0), 2)
        })

    # Top products by revenue
    prod_q = db.query(
        Product.name,
        Product.category,
        Product.mrp,
        func.sum(OrderItem.quantity).label("units_sold"),
        func.sum(OrderItem.total_price).label("revenue")
    ).join(OrderItem, Product.sku_id == OrderItem.sku_id)\
     .join(Order, OrderItem.order_id == Order.order_id)\
     .filter(Order.delivery_status == "DELIVERED")
    prod_q = apply_order_filters(prod_q, start_date, end_date, store_id)
    prod_rows = prod_q.group_by(Product.name, Product.category, Product.mrp).order_by(desc("revenue")).limit(10).all()

    top_products = []
    for p in prod_rows:
        top_products.append({
            "name": p.name,
            "category": p.category,
            "mrp": float(p.mrp),
            "units_sold": int(p.units_sold),
            "revenue": round(float(p.revenue), 2)
        })

    return RevenueAnalyticsResponse(
        total_gmv=round(float(gross_gmv), 2),
        net_revenue=round(float(net_rev), 2),
        avg_order_value=round(float(aov), 2),
        total_discounts=round(float(total_discounts), 2),
        discount_burn_rate=round(float(burn_rate), 2),
        revenue_trends=revenue_trends,
        category_revenue=category_revenue,
        store_revenue=store_revenue,
        top_products=top_products,
        payment_mode_split=payment_mode_split
    )

def get_order_quality_data(db: Session, start_date: Optional[str] = None, end_date: Optional[str] = None, store_id: Optional[str] = None) -> OrderQualityResponse:
    base_orders = db.query(Order)
    base_orders = apply_order_filters(base_orders, start_date, end_date, store_id)
    total_orders = base_orders.count()

    cncl_q = db.query(Cancellation).join(Order, Cancellation.order_id == Order.order_id)
    cncl_q = apply_order_filters(cncl_q, start_date, end_date, store_id)

    total_cncl = cncl_q.count()
    cncl_rate = round((total_cncl * 100.0 / total_orders), 2) if total_orders > 0 else 0.0
    total_refunds = cncl_q.with_entities(func.sum(Cancellation.refund_amount)).scalar() or 0.0

    # Reasons
    reason_rows = cncl_q.with_entities(
        Cancellation.reason,
        func.count(Cancellation.cancellation_id).label("count"),
        func.sum(Cancellation.refund_amount).label("refunds")
    ).group_by(Cancellation.reason).order_by(desc("count")).all()

    cancellation_reasons = []
    for r in reason_rows:
        cancellation_reasons.append({
            "reason": r.reason,
            "count": int(r.count),
            "refunds": round(float(r.refunds or 0.0), 2)
        })

    # Cancelled By
    by_rows = cncl_q.with_entities(
        Cancellation.cancelled_by,
        func.count(Cancellation.cancellation_id).label("count")
    ).group_by(Cancellation.cancelled_by).order_by(desc("count")).all()

    cancelled_by_split = []
    for b in by_rows:
        cancelled_by_split.append({
            "source": b.cancelled_by,
            "count": int(b.count),
            "share_pct": round((b.count * 100.0 / (total_cncl or 1)), 1)
        })

    # Defect Types
    defect_rows = cncl_q.filter(Cancellation.defect_type.isnot(None))\
                        .with_entities(
                            Cancellation.defect_type,
                            func.count(Cancellation.cancellation_id).label("count"),
                            func.sum(Cancellation.refund_amount).label("refunds")
                        ).group_by(Cancellation.defect_type).order_by(desc("count")).all()

    defect_types = []
    for d in defect_rows:
        defect_types.append({
            "defect_type": d.defect_type,
            "count": int(d.count),
            "refunds": round(float(d.refunds or 0.0), 2)
        })

    # Store cancellations
    store_cncl_q = db.query(
        DarkStore.store_id,
        DarkStore.store_name,
        DarkStore.city,
        func.count(Order.order_id).label("total_orders"),
        func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("cancelled_count"),
        func.sum(case((Order.delivery_status == "CANCELLED", Order.net_amount), else_=0.0)).label("lost_revenue")
    ).join(Order, DarkStore.store_id == Order.store_id)
    store_cncl_q = apply_order_filters(store_cncl_q, start_date, end_date, store_id)
    store_cncl_rows = store_cncl_q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city).all()

    store_cancellations = []
    for s in store_cncl_rows:
        tot = s.total_orders or 1
        cn = s.cancelled_count or 0
        store_cancellations.append({
            "store_id": s.store_id,
            "store_name": s.store_name,
            "city": s.city,
            "total_orders": tot,
            "cancelled_orders": cn,
            "cancellation_rate": round((cn * 100.0 / tot), 1),
            "lost_revenue": round(float(s.lost_revenue or 0.0), 2)
        })
    store_cancellations.sort(key=lambda x: x["cancellation_rate"], reverse=True)

    return OrderQualityResponse(
        total_cancellations=total_cncl,
        cancellation_rate=cncl_rate,
        total_refunds=round(float(total_refunds), 2),
        cancellation_reasons=cancellation_reasons,
        cancelled_by_split=cancelled_by_split,
        defect_types=defect_types,
        store_cancellations=store_cancellations
    )
