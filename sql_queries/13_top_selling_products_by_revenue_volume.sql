-- ==============================================================================
-- Query 13: Top 10 Selling Products by Revenue & Volume within Each Category
-- Business Problem:
--   Merchandisers need to know the top performing hero SKUs per category to ensure
--   contractual bulk procurement discounts and avoid stock shortages.
-- Techniques: INNER JOIN, Multiple Joins, CTE, Window Functions (DENSE_RANK PARTITION BY).
-- ==============================================================================

WITH ProductPerformance AS (
    SELECT 
        p.category,
        p.sku_id,
        p.name AS product_name,
        p.brand,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.total_price), 2) AS revenue_generated,
        ROUND(SUM(oi.total_price - (oi.quantity * p.cost_price)), 2) AS category_profit_contribution
    FROM products p
    INNER JOIN order_items oi ON p.sku_id = oi.sku_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY p.category, p.sku_id, p.name, p.brand
),
RankedSKUs AS (
    SELECT 
        category,
        sku_id,
        product_name,
        brand,
        units_sold,
        revenue_generated,
        category_profit_contribution,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY revenue_generated DESC) AS revenue_rank_in_cat,
        DENSE_RANK() OVER (PARTITION BY category ORDER BY units_sold DESC) AS volume_rank_in_cat
    FROM ProductPerformance
)
SELECT 
    category,
    revenue_rank_in_cat,
    product_name,
    brand,
    units_sold,
    revenue_generated,
    category_profit_contribution
FROM RankedSKUs
WHERE revenue_rank_in_cat <= 3
ORDER BY category, revenue_rank_in_cat ASC;
