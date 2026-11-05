-- ==============================================================================
-- Query 20: Revenue Leakage, Discount Margin Erosion & Delivery Subsidies
-- Business Problem:
--   Quantify leakage caused by: order cancellations, refunds, free delivery subsidies,
--   and promotional discounts relative to Gross Merchandise Value.
-- Techniques: CTE, Aggregations, Window Functions (SUM OVER), Multi-term financial balance.
-- ==============================================================================

WITH FinancialComponents AS (
    SELECT 
        ROUND(SUM(total_amount), 2) AS gross_gmv_attempted,
        ROUND(SUM(CASE WHEN delivery_status = 'CANCELLED' THEN total_amount ELSE 0 END), 2) AS cancelled_lost_gmv,
        ROUND(SUM(discount_amount), 2) AS total_discounts_granted,
        ROUND(SUM(CASE WHEN delivery_fee = 0 THEN 15.0 ELSE 0 END), 2) AS free_delivery_subsidized,
        ROUND(SUM(CASE WHEN delivery_status = 'DELIVERED' THEN net_amount ELSE 0 END), 2) AS net_cash_collected
    FROM orders
),
RefundAgg AS (
    SELECT 
        ROUND(SUM(refund_amount), 2) AS total_refunds_processed
    FROM cancellations
)
SELECT 
    f.gross_gmv_attempted,
    f.net_cash_collected,
    f.cancelled_lost_gmv,
    r.total_refunds_processed,
    f.total_discounts_granted,
    f.free_delivery_subsidized,
    ROUND(
        f.cancelled_lost_gmv + r.total_refunds_processed + f.total_discounts_granted + f.free_delivery_subsidized, 
        2
    ) AS total_revenue_leakage_and_burn,
    ROUND(
        ((f.cancelled_lost_gmv + r.total_refunds_processed + f.total_discounts_granted + f.free_delivery_subsidized) * 100.0) / 
        f.gross_gmv_attempted, 2
    ) AS leakage_as_pct_of_gmv
FROM FinancialComponents f
CROSS JOIN RefundAgg r;
