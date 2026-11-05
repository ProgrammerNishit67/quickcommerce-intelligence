# QuickCommerce Intelligence - SQL Analytics Engine Catalog

This directory contains **25 production-grade SQL business analytics queries** modeling the operational complexity of quick-commerce leaders (Blinkit, Zepto, Swiggy Instamart).

## Query Index & Classification

| # | File Name | Business Domain | Key SQL Constructs |
|---|---|---|---|
| **01** | `01_daily_and_monthly_orders.sql` | Executive / Sales | CTE, LAG(), Day-over-Day growth, Date truncation |
| **02** | `02_revenue_by_store.sql` | Store Performance | INNER JOIN, DENSE_RANK(), SUM() OVER() window share |
| **03** | `03_average_order_value_trends.sql` | Revenue / CRM | Multi-table JOIN, Partitioned RANK(), AOV analysis |
| **04** | `04_delivery_sla_compliance.sql` | Logistics & SLA | On-time delivery rate %, RANK() OVER(), Breach metrics |
| **05** | `05_delayed_orders_root_cause.sql` | Delivery Operations | Multi-table JOIN, Severity CASE WHEN buckets, Delay analysis |
| **06** | `06_hourly_order_delivery_heatmap.sql` | Fleet Management | Hour extraction, Operational time-band classification |
| **07** | `07_delivery_partner_efficiency_ranking.sql` | Rider Operations | ROW_NUMBER(), Performance badges, Speed vs SLA metrics |
| **08** | `08_inventory_turnover_ratio.sql` | Supply Chain | COGS, Days Sales of Inventory (DSI), Turnover ratios |
| **09** | `09_stockout_frequency_and_lost_sales.sql` | Inventory Control | Stock health classification, Estimated lost sales revenue |
| **10** | `10_fast_moving_vs_slow_moving_skus.sql` | Merchandising | ABC velocity classification, Cumulative volume percent |
| **11** | `11_stock_replenishment_priority.sql` | Procurement | Automated suggested replenishment units & budget priority |
| **12** | `12_category_revenue_contribution.sql` | Profitability | Gross margin %, Revenue share window SUM OVER() |
| **13** | `13_top_selling_products_by_revenue_volume.sql` | Catalog Strategy | DENSE_RANK() PARTITION BY category (Hero SKUs) |
| **14** | `14_discount_elasticity_and_burn_rate.sql` | Marketing Finance | Discount burn rate %, Basket size vs subsidy elasticity |
| **15** | `15_cancellation_rate_by_stage_and_store.sql` | Quality & Loss | Lost GMV, Cancellation rate %, DENSE_RANK() |
| **16** | `16_refund_and_item_defect_analysis.sql` | Customer Trust | Defect types (Damaged vs Missing), Refund liabilities |
| **17** | `17_repeat_customer_cohort_retention.sql` | Customer Loyalty | Loyalty cohorts (Power Loyalist to Trial), GMV share |
| **18** | `18_rfm_customer_segmentation.sql` | CRM Segmentation | NTILE(4) Recency, Frequency, Monetary scoring matrix |
| **19** | `19_store_performance_rankings_composite.sql` | Store Benchmarking | Multi-factor weighted composite scoring model |
| **20** | `20_revenue_leakage_and_margin_erosion.sql` | Unit Economics | Comprehensive financial leakage reconciliation |
| **21** | `21_rolling_7day_moving_average_orders.sql` | Demand Forecasting | AVG() OVER (ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) |
| **22** | `22_rider_utilization_and_idle_times.sql` | Fleet Optimization | Throughput per rider, Capacity shortage vs surplus |
| **23** | `23_peak_hour_bottleneck_detection.sql` | Real-Time Ops | Peak hour SLA degradation (>15% breach) alerts |
| **24** | `24_dark_store_catchment_density.sql` | Dark Store Ops | Hourly throughput vs designed dark store capacity |
| **25** | `25_executive_scorecard_summary.sql` | Strategic Scorecard | Master KPI synthesis (GMV, AOV, SLA, Stockout, Fleet) |

## Query Execution
All queries can be executed directly against the platform's PostgreSQL or SQLite database using standard SQL clients or via the backend Python analytics engine:
```bash
python -m pytest backend/tests/test_sql_metrics.py -v
```
