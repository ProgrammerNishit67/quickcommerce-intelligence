-- ==============================================================================
-- Query 12: Category Revenue Contribution and Gross Margin Analytics
-- Business Problem:
--   Evaluate margin profitability across product categories. Some categories (Snacks)
--   have high volume but tight margins, while Personal Care offers high margin percentages.
-- Techniques: INNER JOIN, Multi-table Join, CTE, Window Functions (SUM OVER), Aggregations.
-- ==============================================================================

WITH CategorySales AS (
    SELECT 
        p.category,
        COUNT(DISTINCT o.order_id) AS distinct_orders,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.total_price), 2) AS gross_sales_value,
        ROUND(SUM(oi.quantity * p.cost_price), 2) AS total_cost_of_goods,
        ROUND(SUM(oi.total_price - (oi.quantity * p.cost_price)), 2) AS gross_profit
    FROM order_items oi
    INNER JOIN orders o ON oi.order_id = o.order_id
    INNER JOIN products p ON oi.sku_id = p.sku_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY p.category
)
SELECT 
    category,
    distinct_orders,
    total_units_sold,
    gross_sales_value,
    total_cost_of_goods,
    gross_profit,
    ROUND((gross_profit * 100.0) / NULLIF(gross_sales_value, 0), 2) AS gross_margin_pct,
    ROUND((gross_sales_value * 100.0) / SUM(gross_sales_value) OVER (), 2) AS category_revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY gross_profit DESC) AS profit_rank
FROM CategorySales
ORDER BY gross_sales_value DESC;
