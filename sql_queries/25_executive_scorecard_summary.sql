-- ==============================================================================
-- Query 25: Executive Scorecard Summary - Top-Level Strategic KPIs
-- Business Problem:
--   Generate a single consolidated executive summary view of the quick commerce operation:
--   Total GMV, Net Revenue, Orders, Delivery SLA Adherence %, AOV, Cancellation Rate %,
--   Active Store Fleet, and Stockout Prevalence.
-- Techniques: CTE, Cross Joins, Complex Aggregations, Window Functions.
-- ==============================================================================

WITH OrderMetrics AS (
    SELECT 
        COUNT(order_id) AS total_orders,
        SUM(CASE WHEN delivery_status = 'DELIVERED' THEN 1 ELSE 0 END) AS delivered_orders,
        SUM(CASE WHEN delivery_status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(total_amount), 2) AS total_gmv,
        ROUND(SUM(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE 0 END), 2) AS net_revenue,
        ROUND(AVG(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE NULL END), 2) AS average_order_value,
        ROUND(AVG(CASE WHEN delivery_status = 'DELIVERED' THEN delivery_time_minutes ELSE NULL END), 1) AS avg_delivery_time_mins,
        ROUND(
            (SUM(CASE WHEN delivery_status = 'DELIVERED' AND is_sla_breached = 0 THEN 1 ELSE 0 END) * 100.0) / 
            NULLIF(SUM(CASE WHEN delivery_status = 'DELIVERED' THEN 1 ELSE 0 END), 0), 2
        ) AS on_time_delivery_rate_pct,
        ROUND(
            (SUM(CASE WHEN delivery_status = 'CANCELLED' THEN 1 ELSE 0 END) * 100.0) / 
            NULLIF(COUNT(order_id), 0), 2
        ) AS cancellation_rate_pct
    FROM orders
),
InventoryMetrics AS (
    SELECT 
        COUNT(inventory_id) AS total_inventory_records,
        SUM(CASE WHEN stockout_flag = 1 THEN 1 ELSE 0 END) AS stockout_count,
        ROUND(
            (SUM(CASE WHEN stockout_flag = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(inventory_id), 2
        ) AS stockout_rate_pct
    FROM inventory
),
StoreMetrics AS (
    SELECT 
        COUNT(store_id) AS active_dark_stores,
        SUM(active_riders_allocated) AS total_fleet_riders
    FROM dark_stores
    WHERE status = 'ACTIVE'
)
SELECT 
    o.total_orders,
    o.delivered_orders,
    o.cancelled_orders,
    o.total_gmv,
    o.net_revenue,
    o.average_order_value,
    o.avg_delivery_time_mins,
    o.on_time_delivery_rate_pct,
    o.cancellation_rate_pct,
    s.active_dark_stores,
    s.total_fleet_riders,
    i.stockout_rate_pct
FROM OrderMetrics o
CROSS JOIN InventoryMetrics i
CROSS JOIN StoreMetrics s;
