-- ==============================================================================
-- Query 22: Rider Utilization Rate, Active Trips vs Idle Capacity
-- Business Problem:
--   Dark store fleet costs represent a huge operational expense.
--   Compute daily trip throughput per active rider and compare capacity against demand.
-- Techniques: INNER JOIN, Multi-table Joins, CTE, Window Functions (DENSE_RANK).
-- ==============================================================================

WITH StoreRiderCapacity AS (
    SELECT 
        s.store_id,
        s.store_name,
        s.city,
        s.active_riders_allocated,
        COUNT(o.order_id) AS total_delivered_orders,
        ROUND(AVG(o.delivery_time_minutes), 1) AS avg_delivery_minutes
    FROM dark_stores s
    LEFT JOIN orders o ON s.store_id = o.store_id AND o.delivery_status = 'DELIVERED'
    GROUP BY s.store_id, s.store_name, s.city, s.active_riders_allocated
)
SELECT 
    store_id,
    store_name,
    city,
    active_riders_allocated,
    total_delivered_orders,
    avg_delivery_minutes,
    ROUND((total_delivered_orders * 1.0) / NULLIF(active_riders_allocated, 0), 1) AS orders_per_rider_capacity,
    CASE 
        WHEN (total_delivered_orders * 1.0) / NULLIF(active_riders_allocated, 0) > 30 THEN 'Overutilized / Rider Shortage'
        WHEN (total_delivered_orders * 1.0) / NULLIF(active_riders_allocated, 0) < 18 THEN 'Underutilized / Surplus Fleet'
        ELSE 'Balanced Fleet'
    END AS fleet_status,
    DENSE_RANK() OVER (ORDER BY (total_delivered_orders * 1.0) / NULLIF(active_riders_allocated, 0) DESC) AS utilization_rank
FROM StoreRiderCapacity
ORDER BY orders_per_rider_capacity DESC;
