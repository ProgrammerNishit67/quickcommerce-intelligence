-- ==============================================================================
-- Query 24: Dark Store Catchment Density & Hourly Order Velocity Throughput
-- Business Problem:
--   Measure dark store capacity utilization by contrasting peak order hours against
--   designed order packing capacity per hour.
-- Techniques: INNER JOIN, CTE, CASE WHEN, Window Function (PERCENT_RANK / RANK).
-- ==============================================================================

WITH HourlyStoreLoad AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.capacity_orders_per_hour,
        DATE(o.order_timestamp) AS order_date,
        CAST(strftime('%H', o.order_timestamp) AS INTEGER) AS order_hour,
        COUNT(o.order_id) AS orders_handled
    FROM dark_stores s
    INNER JOIN orders o ON s.store_id = o.store_id
    GROUP BY s.store_id, s.store_name, s.capacity_orders_per_hour, order_date, order_hour
)
SELECT 
    store_name,
    capacity_orders_per_hour,
    ROUND(AVG(orders_handled), 1) AS avg_hourly_throughput,
    MAX(orders_handled) AS max_peak_hourly_load,
    ROUND((MAX(orders_handled) * 100.0) / capacity_orders_per_hour, 1) AS max_capacity_utilization_pct,
    DENSE_RANK() OVER (ORDER BY MAX(orders_handled) DESC) AS peak_load_rank
FROM HourlyStoreLoad
GROUP BY store_name, capacity_orders_per_hour
ORDER BY max_capacity_utilization_pct DESC;
