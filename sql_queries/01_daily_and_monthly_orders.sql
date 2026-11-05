-- ==============================================================================
-- Query 01: Daily and Monthly Order Trajectory & Growth Momentum
-- Business Problem:
--   Executive leadership requires a clear breakdown of daily and monthly order volume,
--   delivered vs cancelled orders, Gross Merchandise Value (GMV), and Net Collected Revenue
--   with day-over-day growth rates to identify seasonality and sales deceleration.
-- Techniques: CTE, Window Functions (LAG), Date Truncation/Formatting, CASE WHEN, Aggregations.
-- ==============================================================================

WITH DailyOrderMetrics AS (
    SELECT 
        DATE(order_timestamp) AS order_date,
        COUNT(order_id) AS total_orders,
        SUM(CASE WHEN delivery_status = 'DELIVERED' THEN 1 ELSE 0 END) AS delivered_orders,
        SUM(CASE WHEN delivery_status = 'CANCELLED' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(total_amount), 2) AS gross_merchandise_value,
        ROUND(SUM(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE 0 END), 2) AS net_revenue,
        ROUND(AVG(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE NULL END), 2) AS daily_aov
    FROM orders
    GROUP BY DATE(order_timestamp)
)
SELECT 
    order_date,
    total_orders,
    delivered_orders,
    cancelled_orders,
    ROUND((cancelled_orders * 100.0) / NULLIF(total_orders, 0), 2) AS cancellation_rate_pct,
    gross_merchandise_value,
    net_revenue,
    daily_aov,
    LAG(total_orders, 1) OVER (ORDER BY order_date) AS prev_day_orders,
    ROUND(
        ((total_orders - LAG(total_orders, 1) OVER (ORDER BY order_date)) * 100.0) / 
        NULLIF(LAG(total_orders, 1) OVER (ORDER BY order_date), 0), 2
    ) AS dod_order_growth_pct
FROM DailyOrderMetrics
ORDER BY order_date DESC;
