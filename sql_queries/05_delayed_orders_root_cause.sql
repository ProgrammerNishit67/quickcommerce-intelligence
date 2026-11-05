-- ==============================================================================
-- Query 05: Root Cause and Impact of Delayed Orders (>15 Mins)
-- Business Problem:
--   Analyse orders experiencing severe delays (>20 mins) vs mild delays (15-20 mins)
--   to detect if rider vehicle types or store dispatch delays drive the bottleneck.
-- Techniques: INNER JOIN, Multi-level CASE WHEN bucket, CTE, Aggregations.
-- ==============================================================================

WITH DelayedOrderBreakdown AS (
    SELECT 
        o.order_id,
        o.store_id,
        s.store_name,
        p.vehicle_type,
        o.delivery_time_minutes,
        o.promised_sla_minutes,
        (o.delivery_time_minutes - o.promised_sla_minutes) AS delay_minutes,
        CASE 
            WHEN o.delivery_time_minutes > 25 THEN 'Severe Delay (>25m)'
            WHEN o.delivery_time_minutes > 20 THEN 'High Delay (20-25m)'
            WHEN o.delivery_time_minutes > 15 THEN 'Mild Delay (15-20m)'
            ELSE 'On-Time'
        END AS delay_severity
    FROM orders o
    INNER JOIN dark_stores s ON o.store_id = s.store_id
    INNER JOIN delivery_partners p ON o.partner_id = p.partner_id
    WHERE o.delivery_status = 'DELIVERED'
)
SELECT 
    delay_severity,
    vehicle_type,
    COUNT(order_id) AS order_count,
    ROUND(AVG(delivery_time_minutes), 1) AS avg_delivery_minutes,
    ROUND(AVG(delay_minutes), 1) AS avg_delay_overshoot,
    ROUND(MAX(delivery_time_minutes), 1) AS max_delay_minutes
FROM DelayedOrderBreakdown
GROUP BY delay_severity, vehicle_type
ORDER BY avg_delivery_minutes DESC;
