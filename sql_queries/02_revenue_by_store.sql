-- ==============================================================================
-- Query 02: Dark Store Revenue Contribution and Rank Analysis
-- Business Problem:
--   Dark store expansion requires benchmarking each facility's total revenue contribution,
--   share of overall business volume, and ranking across operational territories.
-- Techniques: INNER JOIN, Window Functions (SUM OVER, DENSE_RANK), Aggregations.
-- ==============================================================================

WITH StoreSales AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.city,
        s.locality,
        COUNT(o.order_id) AS total_orders,
        SUM(CASE WHEN o.delivery_status = 'DELIVERED' THEN 1 ELSE 0 END) AS delivered_orders,
        ROUND(SUM(CASE WHEN o.delivery_status = 'DELIVERED' THEN o.net_amount ELSE 0 END), 2) AS net_revenue
    FROM dark_stores s
    INNER JOIN orders o ON s.store_id = o.store_id
    GROUP BY s.store_id, s.store_name, s.city, s.locality
)
SELECT 
    store_id,
    store_name,
    city,
    locality,
    total_orders,
    delivered_orders,
    net_revenue,
    ROUND((net_revenue * 100.0) / SUM(net_revenue) OVER (), 2) AS revenue_share_pct,
    DENSE_RANK() OVER (ORDER BY net_revenue DESC) AS revenue_rank_national,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY net_revenue DESC) AS revenue_rank_city
FROM StoreSales
ORDER BY net_revenue DESC;
