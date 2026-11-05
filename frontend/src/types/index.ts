export interface OverviewKPIs {
  total_orders: number;
  total_gmv: number;
  net_revenue: number;
  average_order_value: number;
  average_delivery_time: number;
  on_time_delivery_rate: number;
  cancellation_rate: number;
  active_stores: number;
}

export interface TrendPoint {
  date: string;
  orders: number;
  revenue: number;
  aov: number;
  on_time_rate?: number;
  cancellations?: number;
}

export interface StoreBreakdown {
  store_id: string;
  store_name: string;
  city: string;
  orders: number;
  revenue: number;
  avg_delivery_time: number;
  on_time_rate: number;
  cancellation_rate: number;
}

export interface CategoryBreakdown {
  category: string;
  units_sold: number;
  revenue: number;
  gross_margin_pct: number;
  share_pct: number;
}

export interface OverviewResponse {
  kpis: OverviewKPIs;
  daily_trends: TrendPoint[];
  store_performance: StoreBreakdown[];
  category_performance: CategoryBreakdown[];
}

export interface DeliveryAnalyticsResponse {
  avg_delivery_time: number;
  on_time_rate: number;
  sla_breaches: number;
  sla_breach_rate: number;
  hourly_trends: {
    hour: string;
    orders: number;
    avg_time: number;
    breaches: number;
    breach_rate: number;
  }[];
  store_delivery_performance: {
    store_id: string;
    store_name: string;
    city: string;
    riders: number;
    total_orders: number;
    avg_time: number;
    breaches: number;
    on_time_rate: number;
  }[];
  delay_breakdown: {
    tier: string;
    orders: number;
    percentage: number;
  }[];
  partner_performance: {
    partner_id: string;
    name: string;
    vehicle_type: string;
    rating: number;
    trips: number;
    avg_time: number;
    sla_compliance_pct: number;
  }[];
}

export interface InventoryIntelligenceResponse {
  total_skus: number;
  stockout_count: number;
  stockout_rate: number;
  low_stock_count: number;
  overall_turnover_ratio: number;
  category_inventory: {
    category: string;
    items_count: number;
    units_in_stock: number;
    critical_items: number;
    holding_value: number;
  }[];
  fast_moving_products: {
    sku_id: string;
    name: string;
    category: string;
    mrp: number;
    units_sold: number;
    revenue: number;
  }[];
  slow_moving_products: {
    sku_id: string;
    name: string;
    category: string;
    mrp: number;
    units_sold: number;
    revenue: number;
  }[];
  replenishment_recommendations: {
    store_name: string;
    sku_id: string;
    name: string;
    category: string;
    current_stock: number;
    safety_stock: number;
    reorder_level: number;
    suggested_units: number;
    estimated_cost: number;
    urgency: string;
  }[];
}

export interface RevenueAnalyticsResponse {
  total_gmv: number;
  net_revenue: number;
  avg_order_value: number;
  total_discounts: number;
  discount_burn_rate: number;
  revenue_trends: {
    date: string;
    gmv: number;
    net_revenue: number;
    discounts: number;
    aov: number;
  }[];
  category_revenue: {
    category: string;
    revenue: number;
    units_sold: number;
    margin_pct: number;
  }[];
  store_revenue: {
    store_id: string;
    store_name: string;
    city: string;
    orders: number;
    revenue: number;
    aov: number;
    discounts: number;
  }[];
  top_products: {
    name: string;
    category: string;
    mrp: number;
    units_sold: number;
    revenue: number;
  }[];
  payment_mode_split: {
    mode: string;
    orders: number;
    revenue: number;
  }[];
}

export interface OrderQualityResponse {
  total_cancellations: number;
  cancellation_rate: number;
  total_refunds: number;
  cancellation_reasons: {
    reason: string;
    count: number;
    refunds: number;
  }[];
  cancelled_by_split: {
    source: string;
    count: number;
    share_pct: number;
  }[];
  defect_types: {
    defect_type: string;
    count: number;
    refunds: number;
  }[];
  store_cancellations: {
    store_id: string;
    store_name: string;
    city: string;
    total_orders: number;
    cancelled_orders: number;
    cancellation_rate: number;
    lost_revenue: number;
  }[];
}

export interface StorePerformanceRanking {
  national_rank: number;
  store_id: string;
  store_name: string;
  city: string;
  locality: string;
  riders_allocated: number;
  capacity_per_hour: number;
  total_orders: number;
  delivered_orders: number;
  net_revenue: number;
  aov: number;
  avg_delivery_time: number;
  sla_adherence_pct: number;
  cancellation_rate_pct: number;
  in_stock_rate_pct: number;
  composite_score: number;
}

export interface OperationalAlert {
  id: string;
  title: string;
  category: "DELIVERY" | "CANCELLATION" | "REVENUE" | "INVENTORY" | "STORE";
  severity: "CRITICAL" | "WARNING" | "INFO";
  store_name?: string;
  metric_value: string;
  threshold: string;
  detected_at: string;
  description: string;
  recommended_action: string;
}

export interface BusinessInsight {
  id: string;
  title: string;
  category: string;
  impact_level: "HIGH" | "MEDIUM" | "LOW";
  what_happened: string;
  where_it_happened: string;
  supporting_metrics: string[];
  root_cause_analysis: string;
  recommended_action: string;
}

export interface DataQualityReport {
  total_records: number;
  valid_records: number;
  missing_values_count: number;
  duplicates_detected: number;
  anomalies_detected: number;
  data_quality_score: number;
  issues_summary: string[];
}

export interface FilterState {
  startDate: string;
  endDate: string;
  storeId: string;
  category: string;
  preset: string;
}
