-- ==============================================================================
-- Query 06: Hourly Order & Delivery Congestion Heatmap Matrix
-- Business Problem:
--   Dark store fleet dispatching requires understanding hourly surge times and corresponding
--   delivery times to schedule rider shifts efficiently.
-- Techniques: STRFTIME/Date Part extraction, Aggregations, Window Functions, CASE WHEN.
-- ==============================================================================

SELECT 
    CAST(strftime('%H', order_timestamp) AS INTEGER) AS hour_of_day,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(net_amount), 2) AS total_hourly_revenue,
    ROUND(AVG(delivery_time_minutes), 1) AS avg_delivery_time_min,
    SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) AS sla_breaches,
    ROUND(
        (SUM(CASE WHEN is_sla_breached = 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(order_id), 
        2
    ) AS hourly_breach_rate_pct,
    CASE 
        WHEN CAST(strftime('%H', order_timestamp) AS INTEGER) BETWEEN 7 AND 10 THEN 'Morning Rush'
        WHEN CAST(strftime('%H', order_timestamp) AS INTEGER) BETWEEN 16 AND 19 THEN 'Evening Tea & Snacks'
        WHEN CAST(strftime('%H', order_timestamp) AS INTEGER) BETWEEN 20 AND 23 THEN 'Late Night Dinner'
        ELSE 'Off-Peak'
    END AS operational_time_band
FROM orders
GROUP BY hour_of_day
ORDER BY hour_of_day;
