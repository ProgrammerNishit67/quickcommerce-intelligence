-- ==============================================================================
-- Query 07: Delivery Partner Efficiency, Rating & Speed Ranking
-- Business Problem:
--   Fleet managers need to evaluate rider performance: average delivery time, total orders
--   fulfilled, SLA adherence %, customer rating, and identify top vs bottom deciles.
-- Techniques: INNER JOIN, ROW_NUMBER, NTILE / DENSE_RANK, Window Functions, CASE WHEN.
-- ==============================================================================

WITH PartnerStats AS (
    SELECT 
        p.partner_id,
        p.name AS partner_name,
        p.vehicle_type,
        s.store_name,
        p.rating AS partner_rating,
        COUNT(o.order_id) AS trips_completed,
        ROUND(AVG(o.delivery_time_minutes), 1) AS avg_delivery_minutes,
        SUM(CASE WHEN o.is_sla_breached = 0 THEN 1 ELSE 0 END) AS on_time_trips,
        ROUND(
            (SUM(CASE WHEN o.is_sla_breached = 0 THEN 1 ELSE 0 END) * 100.0) / 
            NULLIF(COUNT(o.order_id), 0), 2
        ) AS rider_sla_compliance_pct
    FROM delivery_partners p
    INNER JOIN orders o ON p.partner_id = o.partner_id
    INNER JOIN dark_stores s ON p.store_id = s.store_id
    WHERE o.delivery_status = 'DELIVERED'
    GROUP BY p.partner_id, p.name, p.vehicle_type, s.store_name, p.rating
    HAVING COUNT(o.order_id) >= 10
)
SELECT 
    partner_id,
    partner_name,
    vehicle_type,
    store_name,
    partner_rating,
    trips_completed,
    avg_delivery_minutes,
    rider_sla_compliance_pct,
    ROW_NUMBER() OVER (ORDER BY rider_sla_compliance_pct DESC, avg_delivery_minutes ASC) AS speed_rank,
    CASE 
        WHEN rider_sla_compliance_pct >= 95.0 THEN 'Star Rider'
        WHEN rider_sla_compliance_pct >= 85.0 THEN 'Consistent Performer'
        ELSE 'Needs Speed Coaching'
    END AS performance_badge
FROM PartnerStats
ORDER BY rider_sla_compliance_pct DESC, avg_delivery_minutes ASC;
