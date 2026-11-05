from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class OverviewKPIs(BaseModel):
    total_orders: int
    total_gmv: float
    net_revenue: float
    average_order_value: float
    average_delivery_time: float
    on_time_delivery_rate: float
    cancellation_rate: float
    active_stores: int

class TrendPoint(BaseModel):
    date: str
    orders: int
    revenue: float
    aov: float
    on_time_rate: Optional[float] = None
    cancellations: Optional[int] = None

class StoreBreakdown(BaseModel):
    store_id: str
    store_name: str
    city: str
    orders: int
    revenue: float
    avg_delivery_time: float
    on_time_rate: float
    cancellation_rate: float

class CategoryBreakdown(BaseModel):
    category: str
    units_sold: int
    revenue: float
    gross_margin_pct: float
    share_pct: float

class OverviewResponse(BaseModel):
    kpis: OverviewKPIs
    daily_trends: List[TrendPoint]
    store_performance: List[StoreBreakdown]
    category_performance: List[CategoryBreakdown]

class DeliveryAnalyticsResponse(BaseModel):
    avg_delivery_time: float
    on_time_rate: float
    sla_breaches: int
    sla_breach_rate: float
    hourly_trends: List[Dict[str, Any]]
    store_delivery_performance: List[Dict[str, Any]]
    delay_breakdown: List[Dict[str, Any]]
    partner_performance: List[Dict[str, Any]]

class InventoryIntelligenceResponse(BaseModel):
    total_skus: int
    stockout_count: int
    stockout_rate: float
    low_stock_count: int
    overall_turnover_ratio: float
    category_inventory: List[Dict[str, Any]]
    fast_moving_products: List[Dict[str, Any]]
    slow_moving_products: List[Dict[str, Any]]
    replenishment_recommendations: List[Dict[str, Any]]

class RevenueAnalyticsResponse(BaseModel):
    total_gmv: float
    net_revenue: float
    avg_order_value: float
    total_discounts: float
    discount_burn_rate: float
    revenue_trends: List[Dict[str, Any]]
    category_revenue: List[Dict[str, Any]]
    store_revenue: List[Dict[str, Any]]
    top_products: List[Dict[str, Any]]
    payment_mode_split: List[Dict[str, Any]]

class OrderQualityResponse(BaseModel):
    total_cancellations: int
    cancellation_rate: float
    total_refunds: float
    cancellation_reasons: List[Dict[str, Any]]
    cancelled_by_split: List[Dict[str, Any]]
    defect_types: List[Dict[str, Any]]
    store_cancellations: List[Dict[str, Any]]

class OperationalAlert(BaseModel):
    id: str
    title: str
    category: str # DELIVERY, CANCELLATION, REVENUE, INVENTORY, STORE
    severity: str # CRITICAL, WARNING, INFO
    store_name: Optional[str] = None
    metric_value: str
    threshold: str
    detected_at: str
    description: str
    recommended_action: str

class BusinessInsight(BaseModel):
    id: str
    title: str
    category: str
    impact_level: str # HIGH, MEDIUM, LOW
    what_happened: str
    where_it_happened: str
    supporting_metrics: List[str]
    root_cause_analysis: str
    recommended_action: str
