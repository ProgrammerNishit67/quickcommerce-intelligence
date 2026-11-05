-- ==============================================================================
-- Query 03: Average Order Value (AOV) Dynamics by Payment Mode & Customer Segment
-- Business Problem:
--   Understand how ticket size varies by payment method (UPI vs Cards vs COD) and customer
--   cohorts to guide promotional subsidies and checkout payment routing.
-- Techniques: INNER JOIN, Multiple-Table Joins, CTE, Window Functions, CASE WHEN.
-- ==============================================================================

WITH SegmentPaymentMetrics AS (
    SELECT 
        c.customer_segment,
        o.payment_mode,
        COUNT(o.order_id) AS order_count,
        ROUND(SUM(o.net_amount), 2) AS total_revenue,
        ROUND(AVG(o.net_amount), 2) AS avg_order_value,
        ROUND(AVG(o.discount_amount), 2) AS avg_discount_per_order
    FROM orders o
    INNER JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY c.customer_segment, o.payment_mode
)
SELECT 
    customer_segment,
    payment_mode,
    order_count,
    total_revenue,
    avg_order_value,
    avg_discount_per_order,
    ROUND((total_revenue * 100.0) / SUM(total_revenue) OVER (PARTITION BY customer_segment), 2) AS pct_segment_revenue,
    RANK() OVER (PARTITION BY customer_segment ORDER BY avg_order_value DESC) AS aov_rank_in_segment
FROM SegmentPaymentMetrics
ORDER BY customer_segment, aov_rank_in_segment;
