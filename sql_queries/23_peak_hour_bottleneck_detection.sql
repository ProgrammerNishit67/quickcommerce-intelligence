-- ==============================================================================
-- Query 23: Peak-Hour Operational Bottleneck & SLA Degradation Detection
-- Business Problem:
--   Detect specific dark stores where peak-hour surge causes SLA breach rates to exceed
--   acceptable operating thresholds (>15%).
-- Techniques: INNER JOIN, CTE, Conditional Window Aggregations, Filtered Partitioning.
-- ==============================================================================

WITH StoreHourlyPerformance AS (
    SELECT 
        s.store_id,
        s.store_name,
        CAST(strftime('%H', o.order_timestamp) AS INTEGER) AS order_hour,
        COUNT(o.order_id) AS orders_in_hour,
        SUM(CASE WHEN o.is_sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
        ROUND(AVG(o.delivery_time_minutes), 1) AS avg_delivery_minutes
    FROM dark_stores s
    INNER JOIN orders o ON s.store_id = o.store_id
    GROUP BY s.store_id, s.store_name, order_hour
)
SELECT 
    store_name,
    order_hour,
    orders_in_hour,
    sla_breaches,
    avg_delivery_minutes,
    ROUND((sla_breaches * 100.0) / NULLIF(orders_in_hour, 0), 2) AS peak_breach_rate_pct,
    CASE 
        WHEN (sla_breaches * 100.0) / NULLIF(orders_in_hour, 0) >= 20.0 THEN 'CRITICAL BOTTLENECK'
        WHEN (sla_breaches * 100.0) / NULLIF(orders_in_hour, 0) >= 12.0 THEN 'ELEVATED DELAY'
        ELSE 'STABLE'
    END AS bottleneck_severity
FROM StoreHourlyPerformance
WHERE orders_in_hour >= 15 AND (sla_breaches * 100.0) / NULLIF(orders_in_hour, 0) >= 15.0
ORDER BY peak_breach_rate_pct DESC, orders_in_hour DESC;
