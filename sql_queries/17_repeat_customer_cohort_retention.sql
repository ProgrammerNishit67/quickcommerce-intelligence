-- ==============================================================================
-- Query 17: Repeat Customer Cohort Retention & Order Frequency Distribution
-- Business Problem:
--   Quick commerce lives and dies by frequency. Classify customer base by order frequency
--   (Single Purchase vs Multi-Order Loyalists) and measure contribution to total GMV.
-- Techniques: INNER JOIN, Subquery, CTE, Window Functions (SUM OVER), CASE WHEN.
-- ==============================================================================

WITH CustomerOrderAggs AS (
    SELECT 
        c.customer_id,
        c.name AS customer_name,
        c.city,
        c.signup_date,
        COUNT(o.order_id) AS lifetime_orders,
        ROUND(SUM(o.net_amount), 2) AS lifetime_spend,
        ROUND(AVG(o.net_amount), 2) AS customer_aov,
        MIN(o.order_timestamp) AS first_order_date,
        MAX(o.order_timestamp) AS last_order_date
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.delivery_status = 'DELIVERED'
    GROUP BY c.customer_id, c.name, c.city, c.signup_date
),
CohortTiers AS (
    SELECT 
        customer_id,
        customer_name,
        city,
        lifetime_orders,
        lifetime_spend,
        customer_aov,
        CASE 
            WHEN lifetime_orders >= 15 THEN 'Power Loyalist (15+ Orders)'
            WHEN lifetime_orders >= 8 THEN 'Frequent Shopper (8-14 Orders)'
            WHEN lifetime_orders >= 3 THEN 'Repeat Customer (3-7 Orders)'
            WHEN lifetime_orders = 1 OR lifetime_orders = 2 THEN 'Trial / Low Frequency (1-2 Orders)'
            ELSE 'Zero Purchases'
        END AS loyalty_cohort
    FROM CustomerOrderAggs
)
SELECT 
    loyalty_cohort,
    COUNT(customer_id) AS total_customers,
    ROUND(SUM(lifetime_orders), 0) AS cohort_total_orders,
    ROUND(SUM(lifetime_spend), 2) AS cohort_total_gmv,
    ROUND(AVG(customer_aov), 2) AS cohort_avg_ticket_size,
    ROUND((SUM(lifetime_spend) * 100.0) / SUM(SUM(lifetime_spend)) OVER (), 2) AS gmv_contribution_pct
FROM CohortTiers
GROUP BY loyalty_cohort
ORDER BY cohort_total_gmv DESC;
