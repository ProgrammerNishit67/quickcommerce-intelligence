-- ==============================================================================
-- Query 10: Fast-Moving vs Slow-Moving SKUs (ABC-Velocity Classification)
-- Business Problem:
--   Categorize catalog into Fast-Moving (Top 20% units sold), Medium-Moving (Next 50%),
--   and Slow-Moving / Dead Stock (Bottom 30%) to optimize shelf space in compact dark stores.
-- Techniques: INNER JOIN, Window Functions (SUM OVER, CUME_DIST / NTILE / PERCENT_RANK), CTE.
-- ==============================================================================

WITH ProductVelocity AS (
    SELECT 
        p.sku_id,
        p.name AS product_name,
        p.category,
        p.mrp,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.total_price), 2) AS total_revenue_generated
    FROM products p
    INNER JOIN order_items oi ON p.sku_id = oi.sku_id
    INNER JOIN orders o ON oi.order_id = o.order_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY p.sku_id, p.name, p.category, p.mrp
),
RankedVelocity AS (
    SELECT 
        sku_id,
        product_name,
        category,
        mrp,
        total_units_sold,
        total_revenue_generated,
        ROW_NUMBER() OVER (ORDER BY total_units_sold DESC) AS sales_volume_rank,
        ROUND((total_units_sold * 100.0) / SUM(total_units_sold) OVER (), 2) AS pct_total_units_sold,
        ROUND((total_revenue_generated * 100.0) / SUM(total_revenue_generated) OVER (), 2) AS pct_total_revenue
    FROM ProductVelocity
)
SELECT 
    sku_id,
    product_name,
    category,
    mrp,
    total_units_sold,
    total_revenue_generated,
    pct_total_units_sold,
    sales_volume_rank,
    CASE 
        WHEN sales_volume_rank <= 10 THEN 'Fast-Moving (High Velocity)'
        WHEN sales_volume_rank <= 25 THEN 'Medium-Moving (Stable)'
        ELSE 'Slow-Moving (Review Stock Depth)'
    END AS movement_velocity_tier
FROM RankedVelocity
ORDER BY sales_volume_rank ASC;
