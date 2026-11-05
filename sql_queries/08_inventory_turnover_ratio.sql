-- ==============================================================================
-- Query 08: Category-Level Inventory Turnover Ratio and Days Sales of Inventory (DSI)
-- Business Problem:
--   Assess how efficiently dark store working capital is deployed across categories.
--   High DSI indicates capital locked in slow stock; low DSI risks stockouts.
-- Techniques: Multiple Joins, CTE, Cost of Goods Sold (COGS) calculation, Window SUM.
-- ==============================================================================

WITH CategorySalesCost AS (
    SELECT 
        p.category,
        ROUND(SUM(oi.quantity * p.cost_price), 2) AS total_cogs,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_sales_value,
        SUM(oi.quantity) AS total_units_sold
    FROM order_items oi
    INNER JOIN orders o ON oi.order_id = o.order_id
    INNER JOIN products p ON oi.sku_id = p.sku_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY p.category
),
CategoryHoldingValue AS (
    SELECT 
        p.category,
        ROUND(SUM(i.current_stock * p.cost_price), 2) AS avg_inventory_holding_value,
        SUM(i.current_stock) AS total_units_in_stock
    FROM inventory i
    INNER JOIN products p ON i.sku_id = p.sku_id
    GROUP BY p.category
)
SELECT 
    s.category,
    s.total_sales_value,
    s.total_cogs,
    h.avg_inventory_holding_value,
    ROUND(s.total_cogs / NULLIF(h.avg_inventory_holding_value, 0), 2) AS inventory_turnover_ratio,
    ROUND((h.avg_inventory_holding_value * 60.0) / NULLIF(s.total_cogs, 0), 1) AS days_sales_of_inventory_dsi,
    DENSE_RANK() OVER (ORDER BY s.total_cogs / NULLIF(h.avg_inventory_holding_value, 0) DESC) AS turnover_velocity_rank
FROM CategorySalesCost s
INNER JOIN CategoryHoldingValue h ON s.category = h.category
ORDER BY inventory_turnover_ratio DESC;
