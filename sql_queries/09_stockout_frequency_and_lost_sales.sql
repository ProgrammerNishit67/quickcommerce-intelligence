-- ==============================================================================
-- Query 09: Stockout Frequency, Critical Shortages & Estimated Lost Sales
-- Business Problem:
--   Stockouts in quick commerce immediately drive cart abandonment.
--   Identify SKUs and stores with chronic zero/below-safety stock and compute estimated lost revenue.
-- Techniques: INNER JOIN, Multiple Joins, CASE WHEN, Window Function (RANK OVER).
-- ==============================================================================

WITH StockAlerts AS (
    SELECT 
        s.store_id,
        s.store_name,
        p.sku_id,
        p.name AS product_name,
        p.category,
        p.mrp,
        i.current_stock,
        i.safety_stock,
        i.reorder_level,
        CASE 
            WHEN i.current_stock = 0 THEN 'OUT_OF_STOCK'
            WHEN i.current_stock <= i.safety_stock THEN 'CRITICAL_LOW'
            WHEN i.current_stock <= i.reorder_level THEN 'REORDER_NOW'
            ELSE 'HEALTHY'
        END AS stock_health_status,
        -- Approximate daily burn rate based on safety stock
        ROUND((i.reorder_level - i.safety_stock) * p.mrp, 2) AS estimated_lost_revenue_potential
    FROM inventory i
    INNER JOIN dark_stores s ON i.store_id = s.store_id
    INNER JOIN products p ON i.sku_id = p.sku_id
    WHERE i.stockout_flag = 1 OR i.current_stock <= i.safety_stock
)
SELECT 
    store_name,
    product_name,
    category,
    current_stock,
    safety_stock,
    stock_health_status,
    mrp,
    estimated_lost_revenue_potential,
    RANK() OVER (PARTITION BY store_name ORDER BY estimated_lost_revenue_potential DESC) AS urgency_rank_in_store
FROM StockAlerts
ORDER BY estimated_lost_revenue_potential DESC;
