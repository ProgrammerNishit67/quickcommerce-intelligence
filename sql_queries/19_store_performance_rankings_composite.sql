-- ==============================================================================
-- Query 19: Store Performance Rankings - Multi-Dimensional Composite Score
-- Business Problem:
--   Rank dark stores using a balanced scorecard: Revenue Volume (35%), Delivery SLA % (30%),
--   Low Cancellation % (20%), and Inventory Health % (15%).
-- Techniques: CTE, Multi-Table Joins, Cross-domain subqueries, Window Functions (DENSE_RANK).
-- ==============================================================================

WITH StoreOrderMetrics AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.city,
        COUNT(o.order_id) AS total_orders,
        ROUND(SUM(CASE WHEN o.delivery_status = 'DELIVERED' THEN o.net_amount ELSE 0 END), 2) AS net_revenue,
        ROUND(
            (SUM(CASE WHEN o.delivery_status = 'DELIVERED' AND o.delivery_time_minutes <= o.promised_sla_minutes THEN 1 ELSE 0 END) * 100.0) /
            NULLIF(SUM(CASE WHEN o.delivery_status = 'DELIVERED' THEN 1 ELSE 0 END), 0), 2
        ) AS sla_adherence_pct,
        ROUND(
            (SUM(CASE WHEN o.delivery_status = 'CANCELLED' THEN 1 ELSE 0 END) * 100.0) /
            NULLIF(COUNT(o.order_id), 0), 2
        ) AS cancellation_rate_pct
    FROM dark_stores s
    LEFT JOIN orders o ON s.store_id = o.store_id
    GROUP BY s.store_id, s.store_name, s.city
),
StoreInventoryMetrics AS (
    SELECT 
        store_id,
        ROUND(
            (SUM(CASE WHEN stockout_flag = 0 THEN 1 ELSE 0 END) * 100.0) / COUNT(inventory_id), 2
        ) AS in_stock_rate_pct
    FROM inventory
    GROUP BY store_id
)
SELECT 
    m.store_id,
    m.store_name,
    m.city,
    m.total_orders,
    m.net_revenue,
    m.sla_adherence_pct,
    m.cancellation_rate_pct,
    i.in_stock_rate_pct,
    ROUND(
        (0.35 * (m.net_revenue / 10000.0)) + 
        (0.30 * m.sla_adherence_pct) + 
        (0.20 * (100.0 - m.cancellation_rate_pct)) + 
        (0.15 * i.in_stock_rate_pct), 2
    ) AS composite_performance_score,
    DENSE_RANK() OVER (
        ORDER BY (
            (0.35 * (m.net_revenue / 10000.0)) + 
            (0.30 * m.sla_adherence_pct) + 
            (0.20 * (100.0 - m.cancellation_rate_pct)) + 
            (0.15 * i.in_stock_rate_pct)
        ) DESC
    ) AS national_store_rank
FROM StoreOrderMetrics m
INNER JOIN StoreInventoryMetrics i ON m.store_id = i.store_id
ORDER BY national_store_rank ASC;
