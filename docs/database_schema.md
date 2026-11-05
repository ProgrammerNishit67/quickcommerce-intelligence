# QuickCommerce Intelligence - Database Entity Relationship (ER) Schema

## Architecture Diagram (Mermaid)

```mermaid
erDiagram
    DARK_STORES ||--o{ ORDERS : fulfills
    DARK_STORES ||--o{ INVENTORY : stocks
    DARK_STORES ||--o{ DELIVERY_PARTNERS : stations
    CUSTOMERS ||--o{ ORDERS : places
    DELIVERY_PARTNERS ||--o{ ORDERS : delivers
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
    PRODUCTS ||--o{ INVENTORY : tracked_as
    ORDERS ||--o| CANCELLATIONS : results_in

    DARK_STORES {
        string store_id PK
        string store_name
        string city
        string locality
        int capacity_orders_per_hour
        float latitude
        float longitude
        int active_riders_allocated
        string status
        datetime created_at
    }

    CUSTOMERS {
        string customer_id PK
        string name
        string email
        string phone
        string city
        datetime signup_date
        string customer_segment
    }

    PRODUCTS {
        string sku_id PK
        string name
        string category
        string subcategory
        float mrp
        float cost_price
        string unit
        int shelf_life_days
        boolean is_perishable
        string brand
        string data_source
    }

    DELIVERY_PARTNERS {
        string partner_id PK
        string name
        string vehicle_type
        float rating
        int total_deliveries
        string status
        string store_id FK
        datetime join_date
    }

    ORDERS {
        string order_id PK
        string customer_id FK
        string store_id FK
        string partner_id FK
        datetime order_timestamp
        datetime dispatch_timestamp
        datetime delivery_timestamp
        int promised_sla_minutes
        string delivery_status
        float total_amount
        float discount_amount
        float delivery_fee
        float tip
        float net_amount
        string payment_mode
        float delivery_time_minutes
        boolean is_sla_breached
        string data_source
    }

    ORDER_ITEMS {
        int item_id PK
        string order_id FK
        string sku_id FK
        int quantity
        float unit_price
        float total_price
    }

    INVENTORY {
        int inventory_id PK
        string store_id FK
        string sku_id FK
        int current_stock
        int safety_stock
        int reorder_level
        datetime last_restocked_at
        boolean stockout_flag
    }

    PROMOTIONS {
        string promo_id PK
        string promo_code
        string discount_type
        float discount_value
        float min_order_value
        float max_discount
        int total_redemptions
        boolean is_active
    }

    CANCELLATIONS {
        string cancellation_id PK
        string order_id FK
        string reason
        string cancelled_by
        string refund_status
        float refund_amount
        string defect_type
        datetime cancellation_timestamp
    }
```

## Relational Entity Specifications

| Table Name | Description | Key Business Attributes |
|---|---|---|
| `dark_stores` | Micro-fulfillment dark stores situated within high-density urban catchments. | Store capacity, rider pool allocation, GPS coordinates. |
| `products` | FMCG and grocery product catalog benchmarking Indian retail brands. | Shelf-life, perishability flag, MRP, wholesale cost price. |
| `customers` | Quick commerce consumers segmented by order frequency. | RFM segments, city location, account registration date. |
| `delivery_partners` | Gig delivery riders fulfilling 15-minute quick delivery runs. | Vehicle type (EV / Petrol), customer rating, speed track. |
| `orders` | Transactional master record tracking promised vs actual fulfillment SLAs. | Dispatch timestamp, delivery duration, discount burn, payment method. |
| `order_items` | Line items associated with each customer basket. | Unit sell price, SKU identifier, order quantity. |
| `inventory` | Dark store shelf stock monitoring real-time stockouts. | Safety threshold, reorder trigger point, stockout flag. |
| `promotions` | Campaign discount vouchers and subsidies. | Minimum order value (MOV), discount caps, redemption counts. |
| `cancellations` | Aborted orders, operational defects, and customer refunds. | Cancellation initiator, refund liability, defect category. |
