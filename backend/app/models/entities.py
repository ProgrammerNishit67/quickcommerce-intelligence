from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class DarkStore(Base):
    __tablename__ = "dark_stores"

    store_id = Column(String(50), primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False, index=True)
    locality = Column(String(100), nullable=False)
    capacity_orders_per_hour = Column(Integer, default=120)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    active_riders_allocated = Column(Integer, default=15)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="store")
    inventory_items = relationship("Inventory", back_populates="store")
    partners = relationship("DeliveryPartner", back_populates="store")


class Product(Base):
    __tablename__ = "products"

    sku_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    subcategory = Column(String(50), nullable=False)
    mrp = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    unit = Column(String(20), default="unit")
    shelf_life_days = Column(Integer, default=30)
    is_perishable = Column(Boolean, default=False)
    brand = Column(String(50), nullable=True)
    data_source = Column(String(30), default="public_benchmark")

    order_items = relationship("OrderItem", back_populates="product")
    inventory_items = relationship("Inventory", back_populates="product")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(50), nullable=False, index=True)
    signup_date = Column(DateTime, default=datetime.utcnow)
    customer_segment = Column(String(30), default="Regular")

    orders = relationship("Order", back_populates="customer")


class DeliveryPartner(Base):
    __tablename__ = "delivery_partners"

    partner_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    vehicle_type = Column(String(30), default="EV 2-Wheeler")
    rating = Column(Float, default=4.8)
    total_deliveries = Column(Integer, default=0)
    status = Column(String(20), default="AVAILABLE")
    store_id = Column(String(50), ForeignKey("dark_stores.store_id"), nullable=True)
    join_date = Column(DateTime, default=datetime.utcnow)

    store = relationship("DarkStore", back_populates="partners")
    orders = relationship("Order", back_populates="partner")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    store_id = Column(String(50), ForeignKey("dark_stores.store_id"), nullable=False, index=True)
    partner_id = Column(String(50), ForeignKey("delivery_partners.partner_id"), nullable=True, index=True)
    order_timestamp = Column(DateTime, nullable=False, index=True)
    dispatch_timestamp = Column(DateTime, nullable=True)
    delivery_timestamp = Column(DateTime, nullable=True)
    promised_sla_minutes = Column(Integer, default=15)
    delivery_status = Column(String(30), default="DELIVERED", index=True)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    delivery_fee = Column(Float, default=15.0)
    tip = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    payment_mode = Column(String(30), default="UPI")
    delivery_time_minutes = Column(Float, nullable=True)
    is_sla_breached = Column(Boolean, default=False, index=True)
    data_source = Column(String(30), default="synthetic_operational")

    customer = relationship("Customer", back_populates="orders")
    store = relationship("DarkStore", back_populates="orders")
    partner = relationship("DeliveryPartner", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    cancellation = relationship("Cancellation", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False, index=True)
    sku_id = Column(String(50), ForeignKey("products.sku_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(String(50), ForeignKey("dark_stores.store_id"), nullable=False, index=True)
    sku_id = Column(String(50), ForeignKey("products.sku_id"), nullable=False, index=True)
    current_stock = Column(Integer, nullable=False, default=0)
    safety_stock = Column(Integer, nullable=False, default=10)
    reorder_level = Column(Integer, nullable=False, default=20)
    last_restocked_at = Column(DateTime, default=datetime.utcnow)
    stockout_flag = Column(Boolean, default=False, index=True)

    store = relationship("DarkStore", back_populates="inventory_items")
    product = relationship("Product", back_populates="inventory_items")


class Promotion(Base):
    __tablename__ = "promotions"

    promo_id = Column(String(50), primary_key=True, index=True)
    promo_code = Column(String(30), unique=True, nullable=False)
    discount_type = Column(String(20), default="PERCENTAGE") # PERCENTAGE or FLAT
    discount_value = Column(Float, nullable=False)
    min_order_value = Column(Float, default=199.0)
    max_discount = Column(Float, default=100.0)
    total_redemptions = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class Cancellation(Base):
    __tablename__ = "cancellations"

    cancellation_id = Column(String(50), primary_key=True, index=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), unique=True, nullable=False)
    reason = Column(String(100), nullable=False)
    cancelled_by = Column(String(30), default="CUSTOMER") # CUSTOMER, STORE, RIDER, SYSTEM
    refund_status = Column(String(30), default="REFUNDED")
    refund_amount = Column(Float, default=0.0)
    defect_type = Column(String(50), nullable=True) # MISSING_ITEM, DAMAGED_GOODS, EXTREME_DELAY, OUT_OF_STOCK
    cancellation_timestamp = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="cancellation")
