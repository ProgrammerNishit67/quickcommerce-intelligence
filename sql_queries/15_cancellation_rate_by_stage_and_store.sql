-- ==============================================================================
-- Query 15: Cancellation Rate by Fulfillment Stage, Dark Store and Root Cause
-- Business Problem:
--   Understand when and why orders get cancelled. Distinguish between customer-driven
--   cancellations, store out-of-stock cancellations, and rider logistics breakdowns.
-- Techniques: INNER JOIN, LEFT JOIN, Aggregations, Window Functions (SUM OVER), CASE WHEN.
-- ==============================================================================

WITH StoreCancellations AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.city,
        COUNT(o.order_id) AS total_orders,
        SUM(CASE WHEN o.delivery_status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(CASE WHEN o.delivery_status = 'CANCELLED' THEN o.total_amount ELSE 0 END), 2) AS lost_gross_gmv
    FROM dark_stores s
    INNER JOIN orders o ON s.store_id = o.store_id
    GROUP BY s.store_id, s.store_name, s.city
)
SELECT 
    store_id,
    store_name,
    city,
    total_orders,
    cancelled_orders,
    lost_gross_gmv,
    ROUND((cancelled_orders * 100.0) / NULLIF(total_orders, 0), 2) AS cancellation_rate_pct,
    DENSE_RANK() OVER (ORDER BY (cancelled_orders * 1.0) / NULLIF(total_orders, 0) DESC) AS worst_cancellation_rank
FROM StoreCancellations
ORDER BY cancellation_rate_pct DESC;
