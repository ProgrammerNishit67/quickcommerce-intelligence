-- ==============================================================================
-- Query 18: RFM (Recency, Frequency, Monetary) Customer Segmentation Matrix
-- Business Problem:
--   Segment customer base into actionable CRM cohorts using RFM scoring: Champions,
--   Loyal Customers, Potential Loyalists, At-Risk, and Hibernating.
-- Techniques: CTE, NTILE Window Functions, CASE WHEN, Aggregations.
-- ==============================================================================

WITH CustomerRFM_Raw AS (
    SELECT 
        c.customer_id,
        c.name AS customer_name,
        c.city,
        CAST((JULIANDAY('2026-03-02') - JULIANDAY(MAX(o.order_timestamp))) AS INTEGER) AS recency_days,
        COUNT(o.order_id) AS frequency_orders,
        ROUND(SUM(o.net_amount), 2) AS monetary_spend
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY c.customer_id, c.name, c.city
),
RFM_Scores AS (
    SELECT 
        customer_id,
        customer_name,
        city,
        recency_days,
        frequency_orders,
        monetary_spend,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- recent = higher score
        NTILE(4) OVER (ORDER BY frequency_orders ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_spend ASC) AS m_score
    FROM CustomerRFM_Raw
)
SELECT 
    customer_id,
    customer_name,
    city,
    recency_days,
    frequency_orders,
    monetary_spend,
    (r_score + f_score + m_score) AS composite_rfm_score,
    CASE 
        WHEN (r_score >= 3 AND f_score >= 3 AND m_score >= 3) THEN 'Champions / VIP'
        WHEN (f_score >= 3 AND m_score >= 2) THEN 'Loyal High Value'
        WHEN (r_score >= 3 AND f_score <= 2) THEN 'Recent New Customers'
        WHEN (r_score <= 2 AND f_score >= 3) THEN 'At-Risk High Spenders'
        ELSE 'Hibernating / Needs Re-engagement'
    END AS rfm_segment
FROM RFM_Scores
ORDER BY composite_rfm_score DESC, monetary_spend DESC;
