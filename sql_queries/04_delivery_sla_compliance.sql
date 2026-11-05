-- ==============================================================================
-- Query 04: Delivery SLA Compliance and Breach Rate by Dark Store
-- Business Problem:
--   Quick commerce promises 15-minute delivery. Operations managers need to track
--   on-time fulfillment rates, SLA breach counts, and average delivery durations across hubs.
-- Techniques: INNER JOIN, Conditional Aggregations, CASE WHEN, Window Function (PERCENT_RANK / RANK).
-- ==============================================================================

WITH SLAMetrics AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.city,
        COUNT(o.order_id) AS total_fulfilled_orders,
        SUM(CASE WHEN o.delivery_time_minutes <= o.promised_sla_minutes THEN 1 ELSE 0 END) AS on_time_orders,
        SUM(CASE WHEN o.delivery_time_minutes > o.promised_sla_minutes THEN 1 ELSE 0 END) AS breached_orders,
        ROUND(AVG(o.delivery_time_minutes), 2) AS avg_delivery_minutes,
        ROUND(MIN(o.delivery_time_minutes), 1) AS fastest_delivery_minutes,
        ROUND(MAX(o.delivery_time_minutes), 1) AS slowest_delivery_minutes
    FROM dark_stores s
    INNER JOIN orders o ON s.store_id = o.store_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY s.store_id, s.store_name, s.city
)
SELECT 
    store_id,
    store_name,
    city,
    total_fulfilled_orders,
    on_time_orders,
    breached_orders,
    ROUND((on_time_orders * 100.0) / NULLIF(total_fulfilled_orders, 0), 2) AS on_time_rate_pct,
    ROUND((breached_orders * 100.0) / NULLIF(total_fulfilled_orders, 0), 2) AS sla_breach_rate_pct,
    avg_delivery_minutes,
    RANK() OVER (ORDER BY (on_time_orders * 1.0) / NULLIF(total_fulfilled_orders, 0) DESC) AS sla_rank
FROM SLAMetrics
ORDER BY on_time_rate_pct DESC;
