-- ==============================================================================
-- Query 16: Refund and Item Defect Analysis (Missing Items vs Damaged Goods)
-- Business Problem:
--   Customer trust collapses when orders arrive with missing or damaged goods.
--   Analyse defect rates, total refund liabilities, and identifying operational breakdown origins.
-- Techniques: INNER JOIN, LEFT JOIN, Aggregations, Window Functions (PERCENT_RANK / RANK).
-- ==============================================================================

SELECT 
    c.cancelled_by,
    COALESCE(c.defect_type, 'NO_DEFECT_SPECIFIED') AS defect_type,
    c.reason,
    COUNT(c.cancellation_id) AS total_incidents,
    ROUND(SUM(c.refund_amount), 2) AS total_refund_liability,
    ROUND(AVG(c.refund_amount), 2) AS avg_refund_per_incident,
    ROUND(
        (SUM(c.refund_amount) * 100.0) / SUM(SUM(c.refund_amount)) OVER (), 2
    ) AS pct_total_refund_spend
FROM cancellations c
INNER JOIN orders o ON c.order_id = o.order_id
GROUP BY c.cancelled_by, c.defect_type, c.reason
ORDER BY total_refund_liability DESC;
