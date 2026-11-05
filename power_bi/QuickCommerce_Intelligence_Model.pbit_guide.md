# QuickCommerce Intelligence - Power BI Data Modeling & Dashboard Architecture Guide

This guide details how to construct the enterprise **QuickCommerce Intelligence** dashboard inside Microsoft Power BI Desktop, connecting directly to the PostgreSQL database or importing the seed CSV data pipeline.

---

## 1. Data Model & Star Schema Architecture

The data model adheres to a Kimball-style dimensional star schema optimized for fast Power BI in-memory VertiPaq engine aggregations:

```
                  ┌──────────────────────┐
                  │    dim_customers     │
                  │ (Customer_ID, City)  │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ *
┌──────────────────┐    ┌────┴──────────────────────────────┐    ┌────────────────────┐
│   dim_stores     │ 1  │           fact_orders             │  1 │    dim_calendar    │
│  (Store_ID, City)├────┤ (Order_ID, Store_ID, Customer_ID, ├────┤  (Date, Day, Week) │
└──────────────────┘  * │  Partner_ID, Timestamps, Amounts) │  * └────────────────────┘
                        └────┬──────────────────────────────┘
                             │ 1
                             │
                             │ 1
                        ┌────┴──────────────────────────────┐
                        │         fact_cancellations        │
                        │ (Cancellation_ID, Order_ID, Reason│
                        │   Refund_Amount, Defect_Type)     │
                        └───────────────────────────────────┘

┌──────────────────┐    ┌───────────────────────────────────┐    ┌────────────────────┐
│   dim_products   │ 1  │          fact_inventory           │  1 │     dim_stores     │
│ (SKU_ID, Category├───*│(Inventory_ID, Store_ID, SKU_ID,   ├───*│  (Store_ID, City)  │
│    Cost, MRP)    │    │  Current_Stock, Safety, Reorder)  │    └────────────────────┘
└──────────────────┘    └───────────────────────────────────┘
```

---

## 2. Dashboard Pages & Visual Layout Specifications

### Page 1: Executive C-Suite Scorecard
* **Top Metric Banner:** 4 Multi-row Cards (Total GMV, Net Revenue, Delivered Orders, AOV).
* **Delivery Performance Gauges:** On-Time SLA Rate (Target >= 92%), Average Delivery Duration (14.2 min).
* **Daily Trend Composed Chart:** Line (Net Revenue) + Clustered Column (Total Orders) with 7-Day Rolling Average.
* **Store Revenue Treemap:** Revenue contribution by Dark Store categorized by Metro City.

### Page 2: Delivery Logistics & Fleet Efficiency
* **Hourly Congestion Matrix (Heatmap):** Hour of Day (00-23) vs Dark Store with Conditional Formatting on SLA Breach %.
* **Delivery Bracket Funnel:** `<10m Fast`, `10-15m Standard`, `15-20m Mild Delay`, `20-25m Delay`, `>25m Severe`.
* **Rider Performance Scatter Plot:** X-axis (Average Delivery Minutes), Y-axis (SLA Adherence %), Size (Total Trips Completed), Legend (Vehicle Type).

### Page 3: Inventory Intelligence & Procurement
* **Stock Health Donut Chart:** Zero Stockout vs Critical Safety Stock Breach vs Healthy Stock.
* **Category Capital Matrix:** Bar Chart comparing Inventory Holding Capital vs Cost of Goods Sold.
* **Replenishment Table:** Conditional formatting on `Urgency == 'URGENT_STOCKOUT'` with suggested reorder units.

### Page 4: Revenue & Promotional Margins
* **Waterfall Margin Bridge:** Gross GMV -> (-) Promotional Discounts -> (-) Free Delivery Subsidies -> Net Cash Collected.
* **Payment Mode Donut:** UPI vs Cards vs Wallets vs COD.
* **Top 10 Hero SKU Matrix:** DENSE_RANK() by sales volume and gross contribution margins.

---

## 3. Power BI DirectQuery / Import Connection Setup

1. Open **Power BI Desktop**.
2. Select **Get Data** -> **PostgreSQL database**.
   * Server: `localhost:5432`
   * Database: `quickcommerce`
   * Data Connectivity Mode: `Import` (Recommended for VertiPaq compression) or `DirectQuery`.
3. Load tables: `dark_stores`, `products`, `customers`, `delivery_partners`, `orders`, `order_items`, `inventory`, `cancellations`.
4. Create a calculated **Date/Calendar Table** in Power BI:
   ```dax
   dim_calendar = 
   ADDCOLUMNS(
       CALENDAR(DATE(2026, 1, 1), DATE(2026, 3, 31)),
       "Year", YEAR([Date]),
       "Month", FORMAT([Date], "MMM YYYY"),
       "MonthNo", MONTH([Date]),
       "DayOfWeek", FORMAT([Date], "ddd"),
       "WeekNumber", WEEKNUM([Date])
   )
   ```
5. Paste the DAX measures from `power_bi/dax_measures.dax` into a dedicated `_Measures` table.
