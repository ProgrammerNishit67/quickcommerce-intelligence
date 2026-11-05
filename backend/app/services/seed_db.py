"""
Database Seeding & Ingestion Pipeline
Loads the seed CSV files into SQLite/PostgreSQL with data type validation and referential checks.
"""

import os
import sys

# Ensure backend root is in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.entities import (
    DarkStore,
    Product,
    Customer,
    DeliveryPartner,
    Order,
    OrderItem,
    Inventory,
    Promotion,
    Cancellation
)

# Project root is 4 levels up from this file
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "seed")

def seed_database():
    print(f"Creating all database tables using engine: {engine.url}...")
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # Check if already seeded
        existing_orders = db.query(Order).count()
        if existing_orders > 0:
            print(f"Database already contains {existing_orders} orders. Skipping seeding.")
            return

        print("Ingesting Dark Stores...")
        df_stores = pd.read_csv(os.path.join(DATA_DIR, "dark_stores.csv"))
        for _, row in df_stores.iterrows():
            store = DarkStore(
                store_id=row["store_id"],
                store_name=row["store_name"],
                city=row["city"],
                locality=row["locality"],
                capacity_orders_per_hour=int(row["capacity_orders_per_hour"]),
                latitude=float(row["latitude"]) if pd.notnull(row["latitude"]) else None,
                longitude=float(row["longitude"]) if pd.notnull(row["longitude"]) else None,
                active_riders_allocated=int(row["active_riders_allocated"]),
                status=row["status"]
            )
            db.merge(store)
        db.commit()

        print("Ingesting Products...")
        df_products = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
        for _, row in df_products.iterrows():
            prod = Product(
                sku_id=row["sku_id"],
                name=row["name"],
                category=row["category"],
                subcategory=row["subcategory"],
                mrp=float(row["mrp"]),
                cost_price=float(row["cost_price"]),
                unit=row["unit"],
                shelf_life_days=int(row["shelf_life_days"]),
                is_perishable=bool(row["is_perishable"]),
                brand=row["brand"] if pd.notnull(row["brand"]) else None,
                data_source=row.get("data_source", "public_benchmark")
            )
            db.merge(prod)
        db.commit()

        print("Ingesting Delivery Partners...")
        df_partners = pd.read_csv(os.path.join(DATA_DIR, "delivery_partners.csv"))
        for _, row in df_partners.iterrows():
            partner = DeliveryPartner(
                partner_id=row["partner_id"],
                name=row["name"],
                vehicle_type=row["vehicle_type"],
                rating=float(row["rating"]),
                total_deliveries=int(row["total_deliveries"]),
                status=row["status"],
                store_id=row["store_id"],
                join_date=datetime.strptime(str(row["join_date"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["join_date"]) else datetime.utcnow()
            )
            db.merge(partner)
        db.commit()

        print("Ingesting Customers...")
        df_customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
        for _, row in df_customers.iterrows():
            cust = Customer(
                customer_id=row["customer_id"],
                name=row["name"],
                email=row["email"] if pd.notnull(row["email"]) else None,
                phone=str(row["phone"]) if pd.notnull(row["phone"]) else None,
                city=row["city"],
                signup_date=datetime.strptime(str(row["signup_date"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["signup_date"]) else datetime.utcnow(),
                customer_segment=row.get("customer_segment", "Regular")
            )
            db.merge(cust)
        db.commit()

        print("Ingesting Promotions...")
        df_promos = pd.read_csv(os.path.join(DATA_DIR, "promotions.csv"))
        for _, row in df_promos.iterrows():
            promo = Promotion(
                promo_id=row["promo_id"],
                promo_code=row["promo_code"],
                discount_type=row["discount_type"],
                discount_value=float(row["discount_value"]),
                min_order_value=float(row["min_order_value"]),
                max_discount=float(row["max_discount"]),
                total_redemptions=int(row["total_redemptions"]),
                is_active=bool(row["is_active"])
            )
            db.merge(promo)
        db.commit()

        print("Ingesting Inventory...")
        df_inv = pd.read_csv(os.path.join(DATA_DIR, "inventory.csv"))
        for _, row in df_inv.iterrows():
            inv = Inventory(
                inventory_id=int(row["inventory_id"]),
                store_id=row["store_id"],
                sku_id=row["sku_id"],
                current_stock=int(row["current_stock"]),
                safety_stock=int(row["safety_stock"]),
                reorder_level=int(row["reorder_level"]),
                last_restocked_at=datetime.strptime(str(row["last_restocked_at"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["last_restocked_at"]) else datetime.utcnow(),
                stockout_flag=bool(row["stockout_flag"])
            )
            db.merge(inv)
        db.commit()

        print("Ingesting Orders...")
        df_orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
        for _, row in df_orders.iterrows():
            order = Order(
                order_id=row["order_id"],
                customer_id=row["customer_id"],
                store_id=row["store_id"],
                partner_id=row["partner_id"] if pd.notnull(row["partner_id"]) else None,
                order_timestamp=datetime.strptime(str(row["order_timestamp"]), "%Y-%m-%d %H:%M:%S"),
                dispatch_timestamp=datetime.strptime(str(row["dispatch_timestamp"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["dispatch_timestamp"]) else None,
                delivery_timestamp=datetime.strptime(str(row["delivery_timestamp"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["delivery_timestamp"]) else None,
                promised_sla_minutes=int(row["promised_sla_minutes"]),
                delivery_status=row["delivery_status"],
                total_amount=float(row["total_amount"]),
                discount_amount=float(row["discount_amount"]),
                delivery_fee=float(row["delivery_fee"]),
                tip=float(row["tip"]),
                net_amount=float(row["net_amount"]),
                payment_mode=row["payment_mode"],
                delivery_time_minutes=float(row["delivery_time_minutes"]) if pd.notnull(row["delivery_time_minutes"]) else None,
                is_sla_breached=bool(row["is_sla_breached"]),
                data_source=row.get("data_source", "synthetic_operational")
            )
            db.add(order)
        db.commit()

        print("Ingesting Order Items...")
        df_items = pd.read_csv(os.path.join(DATA_DIR, "order_items.csv"))
        items_batch = []
        for _, row in df_items.iterrows():
            item = OrderItem(
                item_id=int(row["item_id"]),
                order_id=row["order_id"],
                sku_id=row["sku_id"],
                quantity=int(row["quantity"]),
                unit_price=float(row["unit_price"]),
                total_price=float(row["total_price"])
            )
            items_batch.append(item)
            if len(items_batch) >= 1000:
                db.bulk_save_objects(items_batch)
                db.commit()
                items_batch = []
        if items_batch:
            db.bulk_save_objects(items_batch)
            db.commit()

        print("Ingesting Cancellations...")
        df_cncl = pd.read_csv(os.path.join(DATA_DIR, "cancellations.csv"))
        for _, row in df_cncl.iterrows():
            cncl = Cancellation(
                cancellation_id=row["cancellation_id"],
                order_id=row["order_id"],
                reason=row["reason"],
                cancelled_by=row["cancelled_by"],
                refund_status=row["refund_status"],
                refund_amount=float(row["refund_amount"]),
                defect_type=row["defect_type"] if pd.notnull(row["defect_type"]) else None,
                cancellation_timestamp=datetime.strptime(str(row["cancellation_timestamp"]), "%Y-%m-%d %H:%M:%S") if pd.notnull(row["cancellation_timestamp"]) else datetime.utcnow()
            )
            db.merge(cncl)
        db.commit()

        print("Database successfully seeded with all operational tables!")

    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
