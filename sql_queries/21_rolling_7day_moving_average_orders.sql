-- ==============================================================================
-- Query 21: Rolling 7-Day Moving Average of Orders and Revenue Smoother
-- Business Problem:
--   Day-to-day order counts oscillate due to weekday vs weekend swings.
--   A 7-day rolling moving average smooths volatility to uncover true baseline growth.
-- Techniques: CTE, Window Functions (AVG OVER ROWS BETWEEN 6 PRECEDING AND CURRENT ROW).
-- ==============================================================================

WITH DailyTrajectory AS (
    SELECT 
        DATE(order_timestamp) AS order_date,
        COUNT(order_id) AS daily_orders,
        ROUND(SUM(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE 0 END), 2) AS daily_net_revenue
    FROM orders
    GROUP BY DATE(order_timestamp)
)
SELECT 
    order_date,
    daily_orders,
    daily_net_revenue,
    ROUND(
        AVG(daily_orders) OVER (
            ORDER BY order_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 1
    ) AS rolling_7day_avg_orders,
    ROUND(
        AVG(daily_net_revenue) OVER (
            ORDER BY order_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7day_avg_revenue
FROM DailyTrajectory
ORDER BY order_date DESC;
