"""
QuickCommerce Intelligence - Dataset Generator & Seed Pipeline
Generates realistic enterprise quick-commerce operational datasets
inspired by Blinkit, Zepto, and Swiggy Instamart operational dynamics.
"""

import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Ensure reproducible realistic distribution
np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "seed")
RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "raw")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RAW_DIR, exist_ok=True)

# 1. Dark Stores
DARK_STORES = [
    {
        "store_id": "DS-BLR-01",
        "store_name": "Koramangala Hub",
        "city": "Bengaluru",
        "locality": "Koramangala 4th Block",
        "capacity_orders_per_hour": 160,
        "latitude": 12.9352,
        "longitude": 77.6245,
        "active_riders_allocated": 28,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BLR-02",
        "store_name": "Indiranagar Central",
        "city": "Bengaluru",
        "locality": "100 Feet Road, Indiranagar",
        "capacity_orders_per_hour": 140,
        "latitude": 12.9784,
        "longitude": 77.6408,
        "active_riders_allocated": 24,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BLR-03",
        "store_name": "HSR Sector 2 Hub",
        "city": "Bengaluru",
        "locality": "HSR Layout Sector 2",
        "capacity_orders_per_hour": 150,
        "latitude": 12.9116,
        "longitude": 77.6389,
        "active_riders_allocated": 22,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BLR-04",
        "store_name": "Whitefield IT Park",
        "city": "Bengaluru",
        "locality": "ITPB Main Road, Whitefield",
        "capacity_orders_per_hour": 110,
        "latitude": 12.9698,
        "longitude": 77.7499,
        "active_riders_allocated": 16, # Bottleneck store: high traffic & lower riders
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BOM-01",
        "store_name": "Bandra West Pod",
        "city": "Mumbai",
        "locality": "Hill Road, Bandra West",
        "capacity_orders_per_hour": 180,
        "latitude": 19.0596,
        "longitude": 72.8295,
        "active_riders_allocated": 30,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BOM-02",
        "store_name": "Andheri Lokhandwala",
        "city": "Mumbai",
        "locality": "Lokhandwala Complex, Andheri West",
        "capacity_orders_per_hour": 165,
        "latitude": 19.1307,
        "longitude": 72.8267,
        "active_riders_allocated": 26,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-BOM-03",
        "store_name": "Powai Hiranandani",
        "city": "Mumbai",
        "locality": "Central Ave, Hiranandani Powai",
        "capacity_orders_per_hour": 130,
        "latitude": 19.1197,
        "longitude": 72.9051,
        "active_riders_allocated": 20,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-DEL-01",
        "store_name": "Gurgaon Cyber Hub Hub",
        "city": "Delhi NCR",
        "locality": "DLF Cyber City, Sector 24 Gurgaon",
        "capacity_orders_per_hour": 170,
        "latitude": 28.4950,
        "longitude": 77.0895,
        "active_riders_allocated": 27,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-DEL-02",
        "store_name": "Noida Sector 62 Pod",
        "city": "Delhi NCR",
        "locality": "Sector 62 Institutional Area, Noida",
        "capacity_orders_per_hour": 125,
        "latitude": 28.6280,
        "longitude": 77.3649,
        "active_riders_allocated": 18,
        "status": "ACTIVE"
    },
    {
        "store_id": "DS-DEL-03",
        "store_name": "South Extension Hub",
        "city": "Delhi NCR",
        "locality": "South Extension Part II",
        "capacity_orders_per_hour": 140,
        "latitude": 28.5683,
        "longitude": 77.2208,
        "active_riders_allocated": 21,
        "status": "ACTIVE"
    }
]

# 2. Benchmark Catalog Products (Public FMCG Products with accurate prices and categories)
PRODUCTS_CATALOG = [
    # Dairy & Breakfast
    {"sku_id": "SKU-DB-001", "name": "Amul Taaza Fresh Toned Milk 500ml", "category": "Dairy & Breakfast", "subcategory": "Milk", "mrp": 27.0, "cost_price": 23.5, "unit": "500 ml", "shelf_life_days": 2, "is_perishable": True, "brand": "Amul"},
    {"sku_id": "SKU-DB-002", "name": "Nandini Pasteurized Toned Milk 500ml", "category": "Dairy & Breakfast", "subcategory": "Milk", "mrp": 24.0, "cost_price": 20.8, "unit": "500 ml", "shelf_life_days": 2, "is_perishable": True, "brand": "Nandini"},
    {"sku_id": "SKU-DB-003", "name": "Amul Salted Butter 100g", "category": "Dairy & Breakfast", "subcategory": "Butter & Spreads", "mrp": 60.0, "cost_price": 52.0, "unit": "100 g", "shelf_life_days": 180, "is_perishable": False, "brand": "Amul"},
    {"sku_id": "SKU-DB-004", "name": "Modern Brown Bread 400g", "category": "Dairy & Breakfast", "subcategory": "Bread & Bakery", "mrp": 50.0, "cost_price": 41.0, "unit": "400 g", "shelf_life_days": 5, "is_perishable": True, "brand": "Modern"},
    {"sku_id": "SKU-DB-005", "name": "Farm Fresh White Eggs (Pack of 6)", "category": "Dairy & Breakfast", "subcategory": "Eggs", "mrp": 55.0, "cost_price": 44.0, "unit": "6 pcs", "shelf_life_days": 14, "is_perishable": True, "brand": "Eggoz"},
    {"sku_id": "SKU-DB-006", "name": "Mother Dairy Classic Curd 400g", "category": "Dairy & Breakfast", "subcategory": "Curd & Yogurt", "mrp": 35.0, "cost_price": 29.0, "unit": "400 g", "shelf_life_days": 7, "is_perishable": True, "brand": "Mother Dairy"},
    {"sku_id": "SKU-DB-007", "name": "Kellogg's Corn Flakes Original 500g", "category": "Dairy & Breakfast", "subcategory": "Cereals", "mrp": 220.0, "cost_price": 185.0, "unit": "500 g", "shelf_life_days": 270, "is_perishable": False, "brand": "Kellogg's"},
    {"sku_id": "SKU-DB-008", "name": "Epigamia Greek Yogurt Natural 90g", "category": "Dairy & Breakfast", "subcategory": "Curd & Yogurt", "mrp": 50.0, "cost_price": 38.0, "unit": "90 g", "shelf_life_days": 15, "is_perishable": True, "brand": "Epigamia"},

    # Fruits & Vegetables
    {"sku_id": "SKU-FV-001", "name": "Fresh Onion (Pyaz) 1kg", "category": "Fruits & Vegetables", "subcategory": "Fresh Vegetables", "mrp": 38.0, "cost_price": 28.0, "unit": "1 kg", "shelf_life_days": 10, "is_perishable": True, "brand": "Farm Direct"},
    {"sku_id": "SKU-FV-002", "name": "Fresh Potato (Aloo) 1kg", "category": "Fruits & Vegetables", "subcategory": "Fresh Vegetables", "mrp": 32.0, "cost_price": 23.0, "unit": "1 kg", "shelf_life_days": 15, "is_perishable": True, "brand": "Farm Direct"},
    {"sku_id": "SKU-FV-003", "name": "Hybrid Tomato (Tamatar) 500g", "category": "Fruits & Vegetables", "subcategory": "Fresh Vegetables", "mrp": 28.0, "cost_price": 19.0, "unit": "500 g", "shelf_life_days": 6, "is_perishable": True, "brand": "Farm Direct"},
    {"sku_id": "SKU-FV-004", "name": "Fresh Coriander Leaves 100g", "category": "Fruits & Vegetables", "subcategory": "Herbs & Seasoning", "mrp": 15.0, "cost_price": 8.0, "unit": "100 g", "shelf_life_days": 3, "is_perishable": True, "brand": "Farm Direct"},
    {"sku_id": "SKU-FV-005", "name": "Robusta Banana (Pack of 5-6)", "category": "Fruits & Vegetables", "subcategory": "Fresh Fruits", "mrp": 45.0, "cost_price": 32.0, "unit": "6 pcs", "shelf_life_days": 4, "is_perishable": True, "brand": "Fresh Harvest"},
    {"sku_id": "SKU-FV-006", "name": "Washington Royal Gala Apple (4 pcs)", "category": "Fruits & Vegetables", "subcategory": "Fresh Fruits", "mrp": 190.0, "cost_price": 145.0, "unit": "4 pcs", "shelf_life_days": 14, "is_perishable": True, "brand": "Imported"},
    {"sku_id": "SKU-FV-007", "name": "Fresh Lemon (Nimbu) 200g", "category": "Fruits & Vegetables", "subcategory": "Fresh Vegetables", "mrp": 35.0, "cost_price": 22.0, "unit": "200 g", "shelf_life_days": 8, "is_perishable": True, "brand": "Farm Direct"},

    # Snacks & Munchies
    {"sku_id": "SKU-SN-001", "name": "Lay's India's Magic Masala Chips 50g", "category": "Snacks & Munchies", "subcategory": "Chips & Crisps", "mrp": 20.0, "cost_price": 16.2, "unit": "50 g", "shelf_life_days": 120, "is_perishable": False, "brand": "Lay's"},
    {"sku_id": "SKU-SN-002", "name": "Kurkure Masala Munch 82g", "category": "Snacks & Munchies", "subcategory": "Namkeen", "mrp": 20.0, "cost_price": 15.8, "unit": "82 g", "shelf_life_days": 120, "is_perishable": False, "brand": "Kurkure"},
    {"sku_id": "SKU-SN-003", "name": "Haldiram's Bhujia Sev 200g", "category": "Snacks & Munchies", "subcategory": "Namkeen", "mrp": 60.0, "cost_price": 49.0, "unit": "200 g", "shelf_life_days": 180, "is_perishable": False, "brand": "Haldiram's"},
    {"sku_id": "SKU-SN-004", "name": "Act II Instant Popcorn Butter Lovers 85g", "category": "Snacks & Munchies", "subcategory": "Popcorn", "mrp": 40.0, "cost_price": 31.0, "unit": "85 g", "shelf_life_days": 240, "is_perishable": False, "brand": "Act II"},
    {"sku_id": "SKU-SN-005", "name": "Oreo Original Chocolate Sandwich Biscuits 120g", "category": "Snacks & Munchies", "subcategory": "Biscuits & Cookies", "mrp": 35.0, "cost_price": 28.5, "unit": "120 g", "shelf_life_days": 180, "is_perishable": False, "brand": "Cadbury"},
    {"sku_id": "SKU-SN-006", "name": "Doritos Cheese Nachos 60g", "category": "Snacks & Munchies", "subcategory": "Chips & Crisps", "mrp": 30.0, "cost_price": 24.0, "unit": "60 g", "shelf_life_days": 180, "is_perishable": False, "brand": "Doritos"},

    # Instant & Frozen Food
    {"sku_id": "SKU-IF-001", "name": "Maggi 2-Minute Masala Noodles 280g (Pack of 4)", "category": "Instant & Frozen Food", "subcategory": "Noodles & Pasta", "mrp": 56.0, "cost_price": 47.0, "unit": "280 g", "shelf_life_days": 270, "is_perishable": False, "brand": "Nestle Maggi"},
    {"sku_id": "SKU-IF-002", "name": "McCain French Fries 420g", "category": "Instant & Frozen Food", "subcategory": "Frozen Snacks", "mrp": 125.0, "cost_price": 98.0, "unit": "420 g", "shelf_life_days": 365, "is_perishable": False, "brand": "McCain"},
    {"sku_id": "SKU-IF-003", "name": "Knorr Classic Mixed Vegetable Soup 53g", "category": "Instant & Frozen Food", "subcategory": "Soups", "mrp": 45.0, "cost_price": 36.0, "unit": "53 g", "shelf_life_days": 365, "is_perishable": False, "brand": "Knorr"},
    {"sku_id": "SKU-IF-004", "name": "Yummiez Chicken Nuggets 500g", "category": "Instant & Frozen Food", "subcategory": "Frozen Meat & Poultry", "mrp": 240.0, "cost_price": 185.0, "unit": "500 g", "shelf_life_days": 270, "is_perishable": False, "brand": "Godrej Yummiez"},
    {"sku_id": "SKU-IF-005", "name": "Tata Sampann High Protein Ready Poha 80g", "category": "Instant & Frozen Food", "subcategory": "Ready to Eat", "mrp": 45.0, "cost_price": 34.0, "unit": "80 g", "shelf_life_days": 180, "is_perishable": False, "brand": "Tata Sampann"},

    # Beverages
    {"sku_id": "SKU-BV-001", "name": "Coca-Cola Zero Sugar Can 300ml", "category": "Beverages", "subcategory": "Soft Drinks", "mrp": 40.0, "cost_price": 32.0, "unit": "300 ml", "shelf_life_days": 180, "is_perishable": False, "brand": "Coca-Cola"},
    {"sku_id": "SKU-BV-002", "name": "Thums Up Charged 250ml Can", "category": "Beverages", "subcategory": "Soft Drinks", "mrp": 25.0, "cost_price": 19.5, "unit": "250 ml", "shelf_life_days": 180, "is_perishable": False, "brand": "Thums Up"},
    {"sku_id": "SKU-BV-003", "name": "Real Fruit Power Mixed Fruit Juice 1L", "category": "Beverages", "subcategory": "Juices & Drinks", "mrp": 130.0, "cost_price": 105.0, "unit": "1 L", "shelf_life_days": 240, "is_perishable": False, "brand": "Real"},
    {"sku_id": "SKU-BV-004", "name": "Red Bull Energy Drink 250ml", "category": "Beverages", "subcategory": "Energy Drinks", "mrp": 125.0, "cost_price": 102.0, "unit": "250 ml", "shelf_life_days": 365, "is_perishable": False, "brand": "Red Bull"},
    {"sku_id": "SKU-BV-005", "name": "Nescafe Classic Instant Coffee Jar 50g", "category": "Beverages", "subcategory": "Coffee & Tea", "mrp": 185.0, "cost_price": 152.0, "unit": "50 g", "shelf_life_days": 540, "is_perishable": False, "brand": "Nescafe"},
    {"sku_id": "SKU-BV-006", "name": "Bisleri Packaged Drinking Water 5L", "category": "Beverages", "subcategory": "Water", "mrp": 70.0, "cost_price": 54.0, "unit": "5 L", "shelf_life_days": 180, "is_perishable": False, "brand": "Bisleri"},

    # Personal Care
    {"sku_id": "SKU-PC-001", "name": "Dettol Original Germ Protection Soap 125g (Pack of 4)", "category": "Personal Care", "subcategory": "Bath & Body", "mrp": 190.0, "cost_price": 155.0, "unit": "4x125 g", "shelf_life_days": 720, "is_perishable": False, "brand": "Dettol"},
    {"sku_id": "SKU-PC-002", "name": "Colgate Strong Teeth Dental Cream 200g", "category": "Personal Care", "subcategory": "Oral Care", "mrp": 115.0, "cost_price": 92.0, "unit": "200 g", "shelf_life_days": 720, "is_perishable": False, "brand": "Colgate"},
    {"sku_id": "SKU-PC-003", "name": "Head & Shoulders Cool Menthol Anti Dandruff Shampoo 340ml", "category": "Personal Care", "subcategory": "Hair Care", "mrp": 320.0, "cost_price": 255.0, "unit": "340 ml", "shelf_life_days": 720, "is_perishable": False, "brand": "Head & Shoulders"},
    {"sku_id": "SKU-PC-004", "name": "Nivea Soft Light Moisturizer Cream 100ml", "category": "Personal Care", "subcategory": "Skin Care", "mrp": 180.0, "cost_price": 142.0, "unit": "100 ml", "shelf_life_days": 720, "is_perishable": False, "brand": "Nivea"},

    # Home & Cleaning
    {"sku_id": "SKU-HC-001", "name": "Vim Dishwash Liquid Lemon 500ml", "category": "Home & Cleaning", "subcategory": "Dishwashing", "mrp": 120.0, "cost_price": 96.0, "unit": "500 ml", "shelf_life_days": 720, "is_perishable": False, "brand": "Vim"},
    {"sku_id": "SKU-HC-002", "name": "Surf Excel Matic Front Load Detergent Liquid 1L", "category": "Home & Cleaning", "subcategory": "Laundry", "mrp": 230.0, "cost_price": 186.0, "unit": "1 L", "shelf_life_days": 720, "is_perishable": False, "brand": "Surf Excel"},
    {"sku_id": "SKU-HC-003", "name": "Harpic Power Plus Toilet Cleaner Liquid 1L", "category": "Home & Cleaning", "subcategory": "Bathroom Cleaners", "mrp": 215.0, "cost_price": 172.0, "unit": "1 L", "shelf_life_days": 720, "is_perishable": False, "brand": "Harpic"},
    {"sku_id": "SKU-HC-004", "name": "Origami 3 Ply Soft Toilet Paper Roll (Pack of 4)", "category": "Home & Cleaning", "subcategory": "Paper & Wipes", "mrp": 160.0, "cost_price": 120.0, "unit": "4 rolls", "shelf_life_days": 1080, "is_perishable": False, "brand": "Origami"},

    # Pharma & Wellness
    {"sku_id": "SKU-PW-001", "name": "Dolo 650mg Paracetamol Tablets (Strip of 15)", "category": "Pharma & Wellness", "subcategory": "First Aid & OTC", "mrp": 34.0, "cost_price": 27.5, "unit": "15 tabs", "shelf_life_days": 720, "is_perishable": False, "brand": "Micro Labs"},
    {"sku_id": "SKU-PW-002", "name": "Digene Gel Antacid Mint 200ml", "category": "Pharma & Wellness", "subcategory": "Digestion Care", "mrp": 155.0, "cost_price": 125.0, "unit": "200 ml", "shelf_life_days": 540, "is_perishable": False, "brand": "Abbott"},
    {"sku_id": "SKU-PW-003", "name": "Volini Fast Pain Relief Spray 40g", "category": "Pharma & Wellness", "subcategory": "Pain Relief", "mrp": 165.0, "cost_price": 132.0, "unit": "40 g", "shelf_life_days": 720, "is_perishable": False, "brand": "Sun Pharma"},
    {"sku_id": "SKU-PW-004", "name": "Himalaya Purifying Neem Face Wash 100ml", "category": "Pharma & Wellness", "subcategory": "Ayurveda & Herbals", "mrp": 140.0, "cost_price": 110.0, "unit": "100 ml", "shelf_life_days": 720, "is_perishable": False, "brand": "Himalaya"}
]

# 3. Delivery Partners
PARTNER_FIRST_NAMES = ["Ramesh", "Suresh", "Vikram", "Sunil", "Rajesh", "Pooja", "Amit", "Manoj", "Anil", "Deepak",
                       "Sachin", "Vijay", "Kiran", "Pradeep", "Mahesh", "Santosh", "Ravi", "Ashok", "Gaurav", "Rohit"]
PARTNER_LAST_NAMES = ["Kumar", "Sharma", "Yadav", "Singh", "Patil", "Verma", "Shinde", "Gowda", "Das", "Reddy"]

def generate_delivery_partners(stores, count=120):
    partners = []
    vehicle_types = ["EV 2-Wheeler", "Petrol 2-Wheeler", "Bicycle"]
    vehicle_weights = [0.55, 0.40, 0.05]

    for i in range(1, count + 1):
        store = random.choice(stores)
        name = f"{random.choice(PARTNER_FIRST_NAMES)} {random.choice(PARTNER_LAST_NAMES)}"
        partners.append({
            "partner_id": f"DP-{i:04d}",
            "name": name,
            "vehicle_type": random.choices(vehicle_types, weights=vehicle_weights)[0],
            "rating": round(random.uniform(4.2, 5.0), 2),
            "total_deliveries": random.randint(80, 2400),
            "status": random.choice(["AVAILABLE", "ON_DELIVERY", "IDLE", "AVAILABLE", "AVAILABLE"]),
            "store_id": store["store_id"],
            "join_date": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 400))).strftime("%Y-%m-%d %H:%M:%S")
        })
    return partners

# 4. Customers
CUSTOMER_FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Sneha", "Aditya", "Ishita", "Kabir", "Neha", "Varun", "Priya",
                        "Kunal", "Tanvi", "Siddharth", "Meera", "Arjun", "Diya", "Rahul", "Nisha", "Gaurav", "Rhea"]
CUSTOMER_LAST_NAMES = ["Sharma", "Verma", "Gupta", "Patel", "Nair", "Iyer", "Mehta", "Bose", "Joshi", "Chatterjee", "Kulkarni", "Aggarwal"]

def generate_customers(count=600):
    customers = []
    cities = ["Bengaluru", "Mumbai", "Delhi NCR"]
    segments = ["VIP / Power Shopper", "High Frequency", "Regular", "Occasional", "At Risk / Inactive"]
    seg_weights = [0.15, 0.25, 0.35, 0.15, 0.10]

    for i in range(1, count + 1):
        fname = random.choice(CUSTOMER_FIRST_NAMES)
        lname = random.choice(CUSTOMER_LAST_NAMES)
        city = random.choice(cities)
        customers.append({
            "customer_id": f"CUST-{i:05d}",
            "name": f"{fname} {lname}",
            "email": f"{fname.lower()}.{lname.lower()}{i}@example.com",
            "phone": f"+91-{random.randint(7000000000, 9999999999)}",
            "city": city,
            "signup_date": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
            "customer_segment": random.choices(segments, weights=seg_weights)[0]
        })
    return customers

# 5. Promotions
PROMOTIONS = [
    {"promo_id": "PR-01", "promo_code": "QUICK100", "discount_type": "FLAT", "discount_value": 100.0, "min_order_value": 399.0, "max_discount": 100.0, "total_redemptions": 1420, "is_active": True},
    {"promo_id": "PR-02", "promo_code": "FEAST20", "discount_type": "PERCENTAGE", "discount_value": 20.0, "min_order_value": 299.0, "max_discount": 75.0, "total_redemptions": 2890, "is_active": True},
    {"promo_id": "PR-03", "promo_code": "FREEDEL", "discount_type": "FLAT", "discount_value": 15.0, "min_order_value": 149.0, "max_discount": 15.0, "total_redemptions": 5210, "is_active": True},
    {"promo_id": "PR-04", "promo_code": "SUPERBOWL", "discount_type": "PERCENTAGE", "discount_value": 15.0, "min_order_value": 499.0, "max_discount": 120.0, "total_redemptions": 840, "is_active": True},
    {"promo_id": "PR-05", "promo_code": "WELCOME50", "discount_type": "FLAT", "discount_value": 50.0, "min_order_value": 199.0, "max_discount": 50.0, "total_redemptions": 3100, "is_active": True}
]

# 6. Inventory Generation
def generate_inventory(stores, products):
    inventory_records = []
    inv_id = 1
    for store in stores:
        # Certain store might have stockout problems (e.g. DS-BLR-04 Whitefield)
        stockout_bias = 0.15 if store["store_id"] == "DS-BLR-04" else 0.04
        for prod in products:
            is_stockout = random.random() < stockout_bias
            if is_stockout:
                curr_stock = random.randint(0, 3)
            else:
                curr_stock = random.randint(12, 140)

            safety_stock = random.randint(8, 20)
            reorder_lvl = safety_stock + random.randint(10, 25)

            inventory_records.append({
                "inventory_id": inv_id,
                "store_id": store["store_id"],
                "sku_id": prod["sku_id"],
                "current_stock": curr_stock,
                "safety_stock": safety_stock,
                "reorder_level": reorder_lvl,
                "last_restocked_at": (datetime.utcnow() - timedelta(hours=random.randint(2, 48))).strftime("%Y-%m-%d %H:%M:%S"),
                "stockout_flag": (curr_stock <= safety_stock)
            })
            inv_id += 1
    return inventory_records

# 7. Realistic Order & OrderItem Generation
def generate_orders_and_items(stores, products, customers, partners, days_span=60, total_orders=5000):
    orders = []
    order_items = []
    cancellations = []
    item_counter = 1

    end_time = datetime(2026, 3, 1, 23, 59, 59)
    start_time = end_time - timedelta(days=days_span)

    # Hourly distribution probability: peaks at 7-10 AM, 4-7 PM, 8-11 PM
    hourly_weights = [
        0.01, 0.005, 0.005, 0.005, 0.01, 0.02, # 00 - 05
        0.05, 0.08, 0.10, 0.07, 0.05, 0.04,   # 06 - 11 (Morning rush)
        0.04, 0.04, 0.03, 0.03, 0.06, 0.08,   # 12 - 17 (Evening tea)
        0.09, 0.10, 0.09, 0.07, 0.04, 0.02    # 18 - 23 (Dinner/munchies)
    ]
    hours = list(range(24))

    cancellation_reasons = [
        ("Extreme Delivery Delay (>25 mins)", "CUSTOMER", "EXTREME_DELAY"),
        ("Item Out of Stock at Store", "STORE", "OUT_OF_STOCK"),
        ("Customer Changed Mind", "CUSTOMER", None),
        ("Wrong Delivery Address Provided", "CUSTOMER", None),
        ("Rider Vehicle Breakdown", "RIDER", "LOGISTICS_ISSUE"),
        ("Missing / Damaged Items Reported", "CUSTOMER", "DAMAGED_GOODS")
    ]
    cancellation_weights = [0.35, 0.25, 0.15, 0.10, 0.08, 0.07]

    # Map partners by store
    partners_by_store = {}
    for p in partners:
        s_id = p["store_id"]
        if s_id not in partners_by_store:
            partners_by_store[s_id] = []
        partners_by_store[s_id].append(p["partner_id"])

    # Fast moving SKUs (milk, bread, eggs, chips, coke, noodles) have higher probability
    sku_weights = []
    for p in products:
        if p["category"] in ["Dairy & Breakfast", "Snacks & Munchies", "Beverages"]:
            sku_weights.append(5.0)
        elif p["category"] in ["Fruits & Vegetables", "Instant & Frozen Food"]:
            sku_weights.append(3.0)
        else:
            sku_weights.append(1.5)
    sku_weights = np.array(sku_weights) / sum(sku_weights)

    for i in range(1, total_orders + 1):
        order_id = f"ORD-{20260000 + i}"
        customer = random.choice(customers)
        store = random.choice(stores)
        store_id = store["store_id"]

        # Date and hour selection based on distribution
        day_offset = random.randint(0, days_span - 1)
        selected_hour = random.choices(hours, weights=hourly_weights)[0]
        selected_minute = random.randint(0, 59)
        selected_second = random.randint(0, 59)
        order_time = start_time + timedelta(days=day_offset, hours=selected_hour, minutes=selected_minute, seconds=selected_second)

        # Partner
        available_store_partners = partners_by_store.get(store_id, [partners[0]["partner_id"]])
        partner_id = random.choice(available_store_partners)

        # Decide order items (1 to 5 items)
        num_items = random.choices([1, 2, 3, 4, 5, 6], weights=[0.20, 0.35, 0.25, 0.12, 0.05, 0.03])[0]
        selected_skus = np.random.choice(products, size=num_items, replace=False, p=sku_weights)

        subtotal = 0.0
        for sku in selected_skus:
            qty = random.choices([1, 2, 3], weights=[0.75, 0.20, 0.05])[0]
            price = sku["mrp"]
            total_price = round(price * qty, 2)
            subtotal += total_price

            order_items.append({
                "item_id": item_counter,
                "order_id": order_id,
                "sku_id": sku["sku_id"],
                "quantity": qty,
                "unit_price": price,
                "total_price": total_price
            })
            item_counter += 1

        # Delivery SLA & Status
        # DS-BLR-04 (Whitefield) has 20% delay rate due to traffic & rider crunch; others have 7-9%
        delay_chance = 0.22 if store_id == "DS-BLR-04" else 0.08
        is_delayed = (random.random() < delay_chance)

        # Cancellation rate ~ 4.2%
        is_cancelled = (random.random() < 0.045)

        delivery_fee = 15.0 if subtotal < 299 else 0.0
        discount_amount = 0.0
        if subtotal >= 399 and random.random() < 0.40:
            discount_amount = min(round(subtotal * 0.15, 2), 60.0)

        tip = random.choices([0.0, 10.0, 20.0, 30.0], weights=[0.65, 0.20, 0.10, 0.05])[0]
        net_amount = round(subtotal - discount_amount + delivery_fee + tip, 2)

        promised_sla = 15 # standard quick commerce promised SLA in minutes

        if is_cancelled:
            delivery_status = "CANCELLED"
            dispatch_time = order_time + timedelta(minutes=random.randint(2, 6))
            delivery_time = None
            delivery_time_mins = None
            sla_breached = True

            reason_info = random.choices(cancellation_reasons, weights=cancellation_weights)[0]
            cancellations.append({
                "cancellation_id": f"CNCL-{len(cancellations) + 1:05d}",
                "order_id": order_id,
                "reason": reason_info[0],
                "cancelled_by": reason_info[1],
                "refund_status": "REFUNDED",
                "refund_amount": net_amount,
                "defect_type": reason_info[2],
                "cancellation_timestamp": (order_time + timedelta(minutes=random.randint(4, 18))).strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            delivery_status = "DELIVERED"
            dispatch_mins = random.randint(3, 7)
            dispatch_time = order_time + timedelta(minutes=dispatch_mins)

            if is_delayed:
                delivery_time_mins = round(random.uniform(16.5, 32.0), 1)
                sla_breached = True
            else:
                delivery_time_mins = round(random.uniform(7.5, 14.8), 1)
                sla_breached = False

            delivery_time = order_time + timedelta(minutes=delivery_time_mins)

        payment_modes = ["UPI", "Credit Card", "Debit Card", "Wallet", "Cash on Delivery"]
        pay_weights = [0.65, 0.18, 0.08, 0.06, 0.03]

        orders.append({
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "store_id": store_id,
            "partner_id": partner_id,
            "order_timestamp": order_time.strftime("%Y-%m-%d %H:%M:%S"),
            "dispatch_timestamp": dispatch_time.strftime("%Y-%m-%d %H:%M:%S") if dispatch_time else None,
            "delivery_timestamp": delivery_time.strftime("%Y-%m-%d %H:%M:%S") if delivery_time else None,
            "promised_sla_minutes": promised_sla,
            "delivery_status": delivery_status,
            "total_amount": round(subtotal, 2),
            "discount_amount": round(discount_amount, 2),
            "delivery_fee": delivery_fee,
            "tip": tip,
            "net_amount": net_amount,
            "payment_mode": random.choices(payment_modes, weights=pay_weights)[0],
            "delivery_time_minutes": delivery_time_mins,
            "is_sla_breached": sla_breached,
            "data_source": "synthetic_operational"
        })

    return orders, order_items, cancellations

def run_seed_generation():
    print("Generating QuickCommerce Intelligence seed datasets...")

    # 1. Dark Stores
    df_stores = pd.DataFrame(DARK_STORES)
    df_stores.to_csv(os.path.join(DATA_DIR, "dark_stores.csv"), index=False)
    print(f"-> Generated {len(df_stores)} dark stores.")

    # 2. Products Catalog
    df_products = pd.DataFrame(PRODUCTS_CATALOG)
    df_products["data_source"] = "public_benchmark"
    df_products.to_csv(os.path.join(DATA_DIR, "products.csv"), index=False)
    print(f"-> Generated {len(df_products)} public benchmark products.")

    # 3. Delivery Partners
    partners = generate_delivery_partners(DARK_STORES, count=100)
    df_partners = pd.DataFrame(partners)
    df_partners.to_csv(os.path.join(DATA_DIR, "delivery_partners.csv"), index=False)
    print(f"-> Generated {len(df_partners)} delivery partners.")

    # 4. Customers
    customers = generate_customers(count=500)
    df_customers = pd.DataFrame(customers)
    df_customers.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)
    print(f"-> Generated {len(df_customers)} customers.")

    # 5. Promotions
    df_promos = pd.DataFrame(PROMOTIONS)
    df_promos.to_csv(os.path.join(DATA_DIR, "promotions.csv"), index=False)
    print(f"-> Generated {len(df_promos)} promotions.")

    # 6. Inventory
    inventory = generate_inventory(DARK_STORES, PRODUCTS_CATALOG)
    df_inventory = pd.DataFrame(inventory)
    df_inventory.to_csv(os.path.join(DATA_DIR, "inventory.csv"), index=False)
    print(f"-> Generated {len(df_inventory)} inventory records across dark stores.")

    # 7. Orders & Items
    orders, order_items, cancellations = generate_orders_and_items(
        DARK_STORES, PRODUCTS_CATALOG, customers, partners, days_span=60, total_orders=5000
    )
    df_orders = pd.DataFrame(orders)
    df_orders.to_csv(os.path.join(DATA_DIR, "orders.csv"), index=False)
    print(f"-> Generated {len(df_orders)} orders spanning 60 days.")

    df_order_items = pd.DataFrame(order_items)
    df_order_items.to_csv(os.path.join(DATA_DIR, "order_items.csv"), index=False)
    print(f"-> Generated {len(df_order_items)} order items.")

    df_cancellations = pd.DataFrame(cancellations)
    df_cancellations.to_csv(os.path.join(DATA_DIR, "cancellations.csv"), index=False)
    print(f"-> Generated {len(df_cancellations)} cancellations and refunds.")

    # Also generate a sample CSV file for data upload testing in RAW_DIR
    sample_upload = df_orders.head(50).copy()
    sample_upload.to_csv(os.path.join(RAW_DIR, "sample_orders_upload.csv"), index=False)
    print(f"-> Created sample upload file at {os.path.join(RAW_DIR, 'sample_orders_upload.csv')}")

    print("All seed datasets generated successfully!")

if __name__ == "__main__":
    run_seed_generation()
