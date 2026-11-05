# QuickCommerce Intelligence
### End-to-End Quick Commerce Operations Analytics Platform
*Modeled after the high-frequency micro-fulfillment challenges of Blinkit, Zepto, and Swiggy Instamart.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-10b981?style=for-the-badge&logo=github)](https://ProgrammerNishit67.github.io/quickcommerce-intelligence/)
[![Tests](https://img.shields.io/badge/pytest-45%20passed-emerald)](backend/tests/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-blue)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3%20TypeScript-cyan)](frontend/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4%20Enterprise-indigo)](frontend/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%20Compliant-blue)](docs/database_schema.md)
[![SQL Engine](https://img.shields.io/badge/SQL%20Analytics-25%20Queries-amber)](sql_queries/)

> **Live Platform URL:** [https://ProgrammerNishit67.github.io/quickcommerce-intelligence/](https://ProgrammerNishit67.github.io/quickcommerce-intelligence/)  
> **Author GitHub:** [@ProgrammerNishit67](https://github.com/ProgrammerNishit67)

---

## 1. Executive Summary & Business Problem

Quick commerce companies deliver groceries and FMCG goods in **10 to 15 minutes** through localized **dark stores** (micro-fulfillment centers situated within 2-3 km urban radii). Operating under these extreme temporal constraints exposes critical operational vulnerabilities:

* **SLA Breaches:** Rider dispatch latency and peak traffic surges leading to missed 15-minute fulfillment windows.
* **Phantom Stockouts:** Real-time physical shelf counts mismatching app inventory, driving customer cart abandonment.
* **Cancellations & Margin Erosion:** Customer cancellations triggered by delivery delays over 20 minutes, incurring reverse logistics costs and full refund liabilities.
* **Promotion Burn:** Uncalibrated checkout subsidies diluting contribution margins on sub-₹250 baskets.

**QuickCommerce Intelligence** is an enterprise data analytics platform that bridges dark store telemetry, transactional master records, and inventory controls to give operations managers and business analysts complete visibility into fulfillment velocity, financial health, and root-cause bottleneck diagnostics.

---

## 2. Platform Architecture

```
                                  ┌──────────────────────────────────────────────┐
                                  │   React 18 + TypeScript + Tailwind CSS UI    │
                                  │    (10 Operational SaaS Navigation Views)    │
                                  └──────────────────────┬───────────────────────┘
                                                         │ REST APIs / JSON / Streams
                                                         ▼
                                  ┌──────────────────────────────────────────────┐
                                  │            FastAPI Backend Engine            │
                                  │ (Analytics, Anomaly Alerts, Export Service)  │
                                  └──────────┬────────────────────────┬──────────┘
                                             │                        │
                      ┌──────────────────────┴─────────┐   ┌──────────┴──────────────────────┐
                      │    SQL Analytics Engine (25)   │   │  CSV Data Ingestion & Quality   │
                      │ (CTEs, Window, LAG/LEAD, Rank) │   │ (Deduplication, Cleaning, Logs) │
                      └──────────────┬─────────────────┘   └──────────┬──────────────────────┘
                                     │                                │
                                     ▼                                ▼
                          ┌────────────────────────────────────────────────────────┐
                          │         PostgreSQL 16 / SQLite Database Engine         │
                          │   (Orders, Dark Stores, Inventory, Products, Partners) │
                          └────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack

* **Data Engineering & Processing:** Python 3.12, Pandas 2.2, NumPy 2.2, OpenPyXL 3.1.
* **Relational Storage:** PostgreSQL 16 (production/Docker) & high-performance SQLite fallback (local dev).
* **SQL Analytics Engine:** 25 ANSI SQL production queries utilizing CTEs, Window Functions, LAG/LEAD, and composite scorecard ranking.
* **Backend Framework:** FastAPI 0.115 with Pydantic v2 schemas and SQLAlchemy 2.0 ORM.
* **Frontend Web Application:** React 18, TypeScript 5.7, Vite 6, Tailwind CSS 3.4, Recharts 2.15, Lucide Icons.
* **Business Intelligence / Reporting:** Power BI dimensional star schema with DAX measures, automated Excel (`.xlsx`) and CSV report exports.
* **DevOps & Containerization:** Docker, Docker Compose, Multi-stage builds, Nginx reverse proxy.

---

## 4. Key Functional Modules (10 Navigation Views)

| # | Module View | Primary Capabilities & Visual Telemetry |
|---|---|---|
| **1** | **Executive Overview** | Real-time GMV, Net Revenue, Delivered Orders, AOV, Avg Delivery Mins, On-Time SLA %, Cancellation %, 60-day trend chart, Dark store operational matrix. |
| **2** | **Delivery Analytics** | 15-minute SLA breach tracking, hourly congestion heatmaps (Morning rush, Late night munchies), delay tier breakdown, delivery partner efficiency rankings. |
| **3** | **Inventory Intelligence** | Stockout prevalence, safety-stock violations, inventory turnover ratio (COGS vs holding value), Fast-moving (Hero SKUs) vs Dead stock, automated replenishment queue. |
| **4** | **Revenue Analytics** | Topline GMV vs Net Cash Collected, discount subsidy burn rate, category margin contribution, store revenue breakdown, UPI/Card/COD distribution. |
| **5** | **Order Quality** | Defect rates, root-cause cancellation analysis, refund liabilities, cancellation initiator breakdown (Customer vs Store vs Rider). |
| **6** | **Store Performance** | National Dark Store Leaderboard utilizing an objective 4-factor composite scorecard (Revenue 35%, SLA 30%, Low Cancellations 20%, In-Stock 15%). |
| **7** | **Operational Alerts** | Automated anomaly detection engine with rule-based thresholds (CRITICAL, WARNING, INFO) highlighting root causes and recommended dispatch fixes. |
| **8** | **Business Insights** | Structured root-cause analysis cards: *What Happened*, *Where It Happened*, *Supporting Database Metrics*, *RCA Finding*, and *Operations Action Plan*. |
| **9** | **Data Management** | Drag-and-drop CSV upload pipeline, automated deduplication, missing-value imputation, data quality scoring (0-100), and dataset lineage verification. |
| **10** | **Reports & Exports** | 1-Click Excel (`.xlsx`) and CSV downloads for Daily Operations, Delivery SLA, Inventory Exceptions, Store Performance, and Revenue Analysis with live in-app preview. |

---

## 5. Database Schema & Data Lineage

The database stores 10 dark stores, 44 benchmark FMCG products, 100 delivery partners, 500 customers, 5,000 orders, and 12,800+ order line items spanning 60 days of operations.

### Data Provenance & Lineage
To maintain full data integrity, all records are explicitly tagged by origin:
* `public_benchmark`: Verified Indian FMCG grocery catalog items with realistic Indian Rupee MRPs (Amul Milk, Maggi Noodles, Lay's Masala, Coca-Cola Zero, Surf Excel).
* `synthetic_operational`: High-fidelity synthetic operational telemetry modeling realistic peak order hours, delivery dispatch intervals, vehicle types, and SLA breach distributions.
* `csv_upload_ingestion`: Records uploaded via the live data management uploader.

*For full Mermaid Entity-Relationship diagram, refer to [docs/database_schema.md](docs/database_schema.md).*

---

## 6. SQL Analytics Engine Catalog (25 Queries)

All 25 queries reside in the [`sql_queries/`](sql_queries/) directory, fully documented with business context:

1. `01_daily_and_monthly_orders.sql`: Daily order trajectory with Day-over-Day growth momentum via `LAG()`.
2. `02_revenue_by_store.sql`: Dark store revenue share via `SUM() OVER ()` and national/city `DENSE_RANK()`.
3. `03_average_order_value_trends.sql`: AOV ticket size variance by payment channel and customer cohorts.
4. `04_delivery_sla_compliance.sql`: On-time delivery SLA compliance rate by dark store facility.
5. `05_delayed_orders_root_cause.sql`: Delivery duration severity buckets (`<15m`, `15-20m`, `20-25m`, `>25m`).
6. `06_hourly_order_delivery_heatmap.sql`: Hour-of-day order volume and SLA breach congestion matrix.
7. `07_delivery_partner_efficiency_ranking.sql`: Rider speed and SLA compliance rating via `ROW_NUMBER()`.
8. `08_inventory_turnover_ratio.sql`: Days Sales of Inventory (DSI) and COGS working capital turnover.
9. `09_stockout_frequency_and_lost_sales.sql`: Zero-stockout prevalence and estimated unfulfilled sales revenue.
10. `10_fast_moving_vs_slow_moving_skus.sql`: ABC velocity categorization of FMCG catalog.
11. `11_stock_replenishment_priority.sql`: Automated purchase replenishment queue with 2.5x safety stock formula.
12. `12_category_revenue_contribution.sql`: Category gross margin % and contribution margin share.
13. `13_top_selling_products_by_revenue_volume.sql`: Hero SKUs partitioned by category via `DENSE_RANK()`.
14. `14_discount_elasticity_and_burn_rate.sql`: Promotional discount depth vs realized basket ticket size.
15. `15_cancellation_rate_by_stage_and_store.sql`: Lost GMV and cancellation rates by fulfillment dark store.
16. `16_refund_and_item_defect_analysis.sql`: Defect classification (Missing Items, Damaged Goods, Delay).
17. `17_repeat_customer_cohort_retention.sql`: Order frequency cohorts (Power Loyalists to Trial shoppers).
18. `18_rfm_customer_segmentation.sql`: Recency, Frequency, Monetary CRM segmentation using `NTILE(4)`.
19. `19_store_performance_rankings_composite.sql`: Multi-factor weighted composite efficiency scorecard.
20. `20_revenue_leakage_and_margin_erosion.sql`: Comprehensive financial leakage balance sheet.
21. `21_rolling_7day_moving_average_orders.sql`: 7-day rolling moving average demand smoothing.
22. `22_rider_utilization_and_idle_times.sql`: Dark store fleet throughput per active rider.
23. `23_peak_hour_bottleneck_detection.sql`: Real-time detection of dark stores with >15% peak SLA degradation.
24. `24_dark_store_catchment_density.sql`: Peak hourly order throughput vs engineered store packing capacity.
25. `25_executive_scorecard_summary.sql`: Master executive KPI consolidation view.

---

## 7. Installation & Quick Start

### Prerequisites
* Python 3.11+
* Node.js 18+ and npm
* Git

### Option A: Local Native Setup (Recommended for Development)

#### 1. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment and activate
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database (creates tables and ingests seed CSVs)
python app/services/seed_db.py

# Run backend API server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API docs available at `http://localhost:8000/docs`.*

#### 2. Frontend Setup
```bash
# Open a second terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
*Open your browser at `http://localhost:3000` (or `http://localhost:5173`).*

---

### Option B: Local Docker Deployment
```bash
# Build and spin up PostgreSQL, FastAPI backend, and React frontend
docker-compose up --build
```
*Frontend running at `http://localhost:3000`, Backend API at `http://localhost:8000`.*

---

## 8. Automated Testing

The platform includes a rigorous **45-test automated test suite** covering:
* **Metric Calculation Integrity:** Ensures Net Revenue does not double-count cancelled orders, verifies AOV denominators, checks On-Time % + Breach % = 100%, and validates inventory stockout reconciliation.
* **SQL Query Execution:** Executes all 25 SQL files against the active database.
* **API Endpoints:** Verifies responses, status codes, schemas, and live Excel/CSV file generation.
* **Data Ingestion & Deduplication:** Tests primary key deduplication, schema validation, and missing field handling.

To run tests:
```bash
cd backend
.\venv\Scripts\pytest.exe -v
```
**Result:** `45 passed in 8.08s (100% pass rate)`

---

## 9. Power BI Integration

The repository includes a dedicated Power BI module in `power_bi/`:
1. `power_bi/dax_measures.dax`: 20+ production DAX formulas (Rolling 7-Day Averages, GMV, On-Time SLA %, AOV, Stockout Rates).
2. `power_bi/QuickCommerce_Intelligence_Model.pbit_guide.md`: Step-by-step instructions for establishing PostgreSQL DirectQuery/Import connections and building the star schema visual model.

---

## 10. Known Limitations & Roadmap

* **Live Rider GPS Simulation:** Currently computes distance and route congestion based on dark store catchment radius and dispatch timestamps; direct real-time GPS telemetry streaming (MQTT/Kafka) can be added.
* **Automated Purchase Order Dispatch:** Currently generates suggested procurement quantities and budgets; can be integrated with vendor EDI/ERP systems (SAP/Oracle SCM).
