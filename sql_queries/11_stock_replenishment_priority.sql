-- ==============================================================================
-- Query 11: Dark Store Inventory Replenishment Priority Engine
-- Business Problem:
--   Procurement teams need an automated query generating exact purchase replenishment
--   quantities for every store where stock is below reorder threshold.
-- Techniques: INNER JOIN, Multi-table Join, CASE WHEN, Window Function (RANK).
-- ==============================================================================

WITH ReplenishmentQueue AS (
    SELECT 
        s.store_id,
        s.store_name,
        p.sku_id,
        p.name AS product_name,
        p.category,
        i.current_stock,
        i.safety_stock,
        i.reorder_level,
        p.cost_price,
        -- Suggested replenish up to 2.5x reorder level
        CAST(ROUND((i.reorder_level * 2.5) - i.current_stock) AS INTEGER) AS suggested_replenish_units,
        ROUND((ROUND((i.reorder_level * 2.5) - i.current_stock) * p.cost_price), 2) AS estimated_procurement_cost
    FROM inventory i
    INNER JOIN dark_stores s ON i.store_id = s.store_id
    INNER JOIN products p ON i.sku_id = p.sku_id
    WHERE i.current_stock <= i.reorder_level
)
SELECT 
    store_name,
    product_name,
    category,
    current_stock,
    safety_stock,
    reorder_level,
    suggested_replenish_units,
    cost_price,
    estimated_procurement_cost,
    CASE 
        WHEN current_stock <= safety_stock THEN 'URGENT: Stockout Risk'
        ELSE 'NORMAL: Reorder Scheduled'
    END AS replenishment_urgency,
    RANK() OVER (PARTITION BY store_name ORDER BY estimated_procurement_cost DESC) AS priority_in_store
FROM ReplenishmentQueue
ORDER BY replenishment_urgency DESC, estimated_procurement_cost DESC;
