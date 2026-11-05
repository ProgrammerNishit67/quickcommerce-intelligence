-- ==============================================================================
-- Query 14: Promotion Discount Elasticity, Burn Rate and ROI Analysis
-- Business Problem:
--   Marketing spends millions on checkout discounts. Measure how discount depth
--   correlates with net basket size and whether heavy discounts trigger higher unit volumes.
-- Techniques: Subquery / CTE, Aggregations, CASE WHEN, Window Function (PERCENT_RANK / RANK).
-- ==============================================================================

WITH DiscountTiers AS (
    SELECT 
        order_id,
        net_amount,
        discount_amount,
        CASE 
            WHEN discount_amount = 0 THEN 'No Discount'
            WHEN discount_amount <= 25 THEN 'Low Discount (1-25)'
            WHEN discount_amount <= 50 THEN 'Medium Discount (26-50)'
            ELSE 'High Discount (>50)'
        END AS discount_tier
    FROM orders
    WHERE delivery_status = 'DELIVERED'
)
SELECT 
    discount_tier,
    COUNT(order_id) AS order_count,
    ROUND(SUM(net_amount), 2) AS total_realized_revenue,
    ROUND(SUM(discount_amount), 2) AS total_discount_subsidized,
    ROUND(AVG(net_amount), 2) AS avg_net_basket_size,
    ROUND(AVG(discount_amount), 2) AS avg_discount_per_basket,
    ROUND(
        (SUM(discount_amount) * 100.0) / 
        NULLIF(SUM(net_amount + discount_amount), 0), 2
    ) AS discount_burn_rate_pct
FROM DiscountTiers
GROUP BY discount_tier
ORDER BY total_realized_revenue DESC;
