import io
from typing import Optional
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func, case, desc
from app.models.entities import Order, DarkStore, Product, Inventory, Cancellation

def generate_report_dataframe(report_type: str, db: Session, store_id: Optional[str] = None) -> pd.DataFrame:
    if report_type == "daily_ops":
        q = db.query(
            func.date(Order.order_timestamp).label("Date"),
            func.count(Order.order_id).label("Total Orders"),
            func.sum(case((Order.delivery_status == "DELIVERED", 1), else_=0)).label("Delivered Orders"),
            func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("Cancelled Orders"),
            func.sum(Order.total_amount).label("Gross GMV (INR)"),
            func.sum(case((Order.delivery_status == "DELIVERED", Order.net_amount), else_=0.0)).label("Net Revenue (INR)"),
            func.avg(case((Order.delivery_status == "DELIVERED", Order.delivery_time_minutes), else_=None)).label("Avg Delivery Time (Min)"),
            func.sum(case((Order.delivery_status == "DELIVERED", case((Order.is_sla_breached == False, 1), else_=0)), else_=0)).label("On Time Deliveries")
        )
        if store_id and store_id != "all":
            q = q.filter(Order.store_id == store_id)
        rows = q.group_by("Date").order_by(desc("Date")).all()
        data = []
        for r in rows:
            deliv = r[2] or 0
            on_time = round((r[7] * 100.0 / deliv), 1) if deliv > 0 else 0.0
            data.append({
                "Date": str(r[0]),
                "Total Orders": int(r[1]),
                "Delivered Orders": int(deliv),
                "Cancelled Orders": int(r[3] or 0),
                "Gross GMV (INR)": round(float(r[4] or 0.0), 2),
                "Net Revenue (INR)": round(float(r[5] or 0.0), 2),
                "Avg Delivery Time (Min)": round(float(r[6] or 0.0), 1),
                "On-Time SLA Rate (%)": on_time
            })
        return pd.DataFrame(data)

    elif report_type == "delivery_sla":
        q = db.query(
            DarkStore.store_id.label("Store ID"),
            DarkStore.store_name.label("Store Name"),
            DarkStore.city.label("City"),
            func.count(Order.order_id).label("Total Trips"),
            func.avg(Order.delivery_time_minutes).label("Avg Delivery Mins"),
            func.sum(case((Order.is_sla_breached == False, 1), else_=0)).label("On Time Deliveries"),
            func.sum(case((Order.is_sla_breached == True, 1), else_=0)).label("SLA Breaches")
        ).join(Order, DarkStore.store_id == Order.store_id)\
         .filter(Order.delivery_status == "DELIVERED")
        if store_id and store_id != "all":
            q = q.filter(DarkStore.store_id == store_id)
        rows = q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city).all()
        data = []
        for r in rows:
            tot = r[3] or 1
            ot = r[5] or 0
            br = r[6] or 0
            data.append({
                "Store ID": r[0],
                "Store Name": r[1],
                "City": r[2],
                "Total Trips": int(tot),
                "Avg Delivery Mins": round(float(r[4] or 0.0), 1),
                "On-Time Deliveries": int(ot),
                "SLA Breaches": int(br),
                "On-Time SLA Rate (%)": round((ot * 100.0 / tot), 1),
                "Breach Rate (%)": round((br * 100.0 / tot), 1)
            })
        return pd.DataFrame(data)

    elif report_type == "inventory_exception":
        q = db.query(
            DarkStore.store_name.label("Store Name"),
            Product.sku_id.label("SKU ID"),
            Product.name.label("Product Name"),
            Product.category.label("Category"),
            Inventory.current_stock.label("Current Stock"),
            Inventory.safety_stock.label("Safety Stock"),
            Inventory.reorder_level.label("Reorder Level"),
            Product.cost_price.label("Cost Price"),
            Product.mrp.label("MRP")
        ).join(DarkStore, Inventory.store_id == DarkStore.store_id)\
         .join(Product, Inventory.sku_id == Product.sku_id)\
         .filter(Inventory.current_stock <= Inventory.reorder_level)
        if store_id and store_id != "all":
            q = q.filter(DarkStore.store_id == store_id)
        rows = q.order_by(Inventory.current_stock.asc()).all()
        data = []
        for r in rows:
            curr = int(r[4])
            reord = int(r[6])
            suggested = max(0, int((reord * 2.5) - curr))
            status = "OUT_OF_STOCK" if curr == 0 else ("CRITICAL_SAFETY_BREACH" if curr <= int(r[5]) else "REORDER_TRIGGERED")
            data.append({
                "Store Name": r[0],
                "SKU ID": r[1],
                "Product Name": r[2],
                "Category": r[3],
                "Current Stock": curr,
                "Safety Stock": int(r[5]),
                "Reorder Level": reord,
                "Suggested Replenish Units": suggested,
                "Cost Price (INR)": float(r[7]),
                "MRP (INR)": float(r[8]),
                "Estimated Restock Cost (INR)": round(suggested * float(r[7]), 2),
                "Exception Status": status
            })
        return pd.DataFrame(data)

    elif report_type == "store_performance":
        q = db.query(
            DarkStore.store_id.label("Store ID"),
            DarkStore.store_name.label("Store Name"),
            DarkStore.city.label("City"),
            DarkStore.active_riders_allocated.label("Fleet Riders"),
            func.count(Order.order_id).label("Total Orders"),
            func.sum(case((Order.delivery_status == "DELIVERED", Order.net_amount), else_=0.0)).label("Net Revenue (INR)"),
            func.avg(case((Order.delivery_status == "DELIVERED", Order.delivery_time_minutes), else_=None)).label("Avg Delivery Time (Min)"),
            func.sum(case((Order.delivery_status == "DELIVERED", case((Order.is_sla_breached == False, 1), else_=0)), else_=0)).label("On Time Count"),
            func.sum(case((Order.delivery_status == "CANCELLED", 1), else_=0)).label("Cancelled Count")
        ).join(Order, DarkStore.store_id == Order.store_id)
        rows = q.group_by(DarkStore.store_id, DarkStore.store_name, DarkStore.city, DarkStore.active_riders_allocated).all()
        data = []
        for r in rows:
            tot = r[4] or 1
            deliv_orders = tot - (r[8] or 0)
            rev = float(r[5] or 0.0)
            aov = round(rev / deliv_orders, 2) if deliv_orders > 0 else 0.0
            ot_rate = round((r[7] * 100.0 / deliv_orders), 1) if deliv_orders > 0 else 0.0
            cncl_rate = round((r[8] * 100.0 / tot), 1)
            data.append({
                "Store ID": r[0],
                "Store Name": r[1],
                "City": r[2],
                "Fleet Riders": int(r[3]),
                "Total Orders": int(tot),
                "Net Revenue (INR)": round(rev, 2),
                "Average Order Value (INR)": aov,
                "Avg Delivery Time (Min)": round(float(r[6] or 0.0), 1),
                "On-Time SLA Rate (%)": ot_rate,
                "Cancellation Rate (%)": cncl_rate
            })
        return pd.DataFrame(data)

    elif report_type == "revenue_analysis":
        q = db.query(
            Product.category.label("Category"),
            func.count(func.distinct(Order.order_id)).label("Orders Count"),
            func.sum(Order.total_amount).label("Gross Sales Value (INR)"),
            func.sum(Order.discount_amount).label("Discount Subsidies (INR)"),
            func.sum(Order.net_amount).label("Net Realized Revenue (INR)")
        ).join(Order, DarkStore.store_id == Order.store_id)\
         .filter(Order.delivery_status == "DELIVERED")
        rows = q.group_by(Product.category).all()
        data = []
        for r in rows:
            gross = float(r[2] or 0.0)
            disc = float(r[3] or 0.0)
            net = float(r[4] or 0.0)
            burn = round((disc * 100.0 / gross), 1) if gross > 0 else 0.0
            data.append({
                "Category": r[0] if r[0] else "Platform Overall",
                "Orders Count": int(r[1] or 0),
                "Gross Sales (INR)": round(gross, 2),
                "Discount Subsidies (INR)": round(disc, 2),
                "Net Realized Revenue (INR)": round(net, 2),
                "Discount Burn Rate (%)": burn
            })
        return pd.DataFrame(data)

    return pd.DataFrame([{"Message": "Unknown Report Type"}])

def export_report_to_bytes(report_type: str, export_format: str, db: Session, store_id: Optional[str] = None) -> tuple[bytes, str, str]:
    df = generate_report_dataframe(report_type, db, store_id)
    filename = f"QuickCommerce_{report_type}_{export_format}"
    
    if export_format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=report_type[:31], index=False)
        output.seek(0)
        return output.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", f"{filename}.xlsx"
    else:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        return csv_bytes, "text/csv", f"{filename}.csv"
