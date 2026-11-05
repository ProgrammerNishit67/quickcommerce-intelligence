# QuickCommerce Intelligence - Master KPI Dictionary & Metric Reference

This reference documents the primary Operational and Financial Key Performance Indicators (KPIs) utilized across the platform, modeled directly from the unit economics of Blinkit, Zepto, and Swiggy Instamart.

---

### 1. Gross Merchandise Value (GMV)
* **Definition:** The cumulative monetary value of all goods placed by customers across the platform before subtracting discounts, promotional vouchers, or cancellations.
* **Formula:** $\sum \text{total\_amount}$
* **Target Benchmark:** Growth oriented, tracking Gross Topline.

---

### 2. Net Collected Revenue
* **Definition:** Actual cash realized and settled for completed, successfully delivered customer orders, accounting for promotional deductions and excluding cancelled or refunded transactions.
* **Formula:** $\sum_{\text{status} = 'DELIVERED'} \text{net\_amount}$
* **Reconciliation Rule:** Never double count cancelled orders or unfulfilled carts in Net Revenue.

---

### 3. Average Order Value (AOV)
* **Definition:** The average net basket size spent per fulfilled customer delivery.
* **Formula:** $\frac{\text{Net Collected Revenue}}{\text{Total Delivered Orders}}$
* **Benchmark:** Quick Commerce benchmark: ₹280 – ₹450. Low AOV (< ₹250) leads to delivery fee margin erosion.

---

### 4. 15-Minute On-Time Delivery SLA Adherence %
* **Definition:** Percentage of delivered orders where actual fulfillment duration from order placement to customer doorstep is less than or equal to the promised SLA (15 minutes).
* **Formula:** $\frac{\text{Count}(\text{delivery\_time\_minutes} \le \text{promised\_sla\_minutes})}{\text{Total Delivered Orders}} \times 100$
* **Target Benchmark:** $\ge 92.0\%$.

---

### 5. Order Cancellation Rate %
* **Definition:** Percentage of placed orders that were terminated before fulfillment, whether initiated by the customer (delay/mind changed), dark store (stock shortage), or rider.
* **Formula:** $\frac{\text{Total Cancelled Orders}}{\text{Total Placed Orders}} \times 100$
* **Target Benchmark:** $\le 4.0\%$. Rates exceeding 5.5% trigger automated operational alerts.

---

### 6. Zero Stockout Prevalence Rate %
* **Definition:** Proportion of active dark store catalog SKUs whose current available physical stock is 0 units.
* **Formula:** $\frac{\text{Count}(\text{current\_stock} = 0)}{\text{Total Active Inventory SKUs}} \times 100$
* **Target Benchmark:** $\le 3.5\%$. Stockouts in high-frequency FMCG categories immediately trigger shopping cart abandonments.

---

### 7. Days Sales of Inventory (DSI) / Inventory Turnover Ratio
* **Definition:** The frequency with which dark store inventory is sold and replaced over an accounting period.
* **Formula:**
  $$\text{Turnover Ratio} = \frac{\text{Cost of Goods Sold (COGS)}}{\text{Average Inventory Value}}$$
  $$\text{DSI} = \frac{\text{Average Inventory Value} \times 60}{\text{COGS}}$$
* **Target Benchmark:** High velocity: Fresh & Dairy (DSI 1.5 - 3 days); Ambient Groceries (DSI 8 - 14 days).

---

### 8. Discount Burn Rate %
* **Definition:** The share of gross merchandise value absorbed by promotional discounts and seller subsidies.
* **Formula:** $\frac{\text{Total Discount Subsidies Granted}}{\text{Gross Merchandise Value}} \times 100$
* **Target Benchmark:** $\le 10.0\%$. Values over 15% indicate unprofitable growth subsidization.

---

### 9. Composite Dark Store Performance Score (0 - 100)
* **Definition:** A multi-dimensional weighted efficiency index evaluating dark store hub operational health:
  $$\text{Score} = (0.35 \times \text{Revenue Volume}) + (0.30 \times \text{SLA Adherence \%}) + (0.20 \times [100 - \text{Cancellation \%}]) + (0.15 \times \text{In-Stock Rate \%})$$
