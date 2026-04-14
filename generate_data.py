"""
=============================================================
  RETAIL SALES RECOMMENDATION SYSTEM
  Data Generator — Synthetic Monthly Sales Data
=============================================================
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

# ── Product catalogue ──────────────────────────────────────
PRODUCTS = {
    # Electronics
    "Wireless Earbuds":      {"category": "Electronics",   "base_price": 3499,  "base_units": 210},
    "Smart Watch":           {"category": "Electronics",   "base_price": 8999,  "base_units": 130},
    "Bluetooth Speaker":     {"category": "Electronics",   "base_price": 2199,  "base_units": 175},
    "Laptop Stand":          {"category": "Electronics",   "base_price": 1299,  "base_units": 145},
    "USB-C Hub":             {"category": "Electronics",   "base_price": 1599,  "base_units": 190},
    # Apparel
    "Winter Jacket":         {"category": "Apparel",       "base_price": 4599,  "base_units": 95},
    "Running Shoes":         {"category": "Apparel",       "base_price": 3299,  "base_units": 160},
    "Yoga Pants":            {"category": "Apparel",       "base_price": 1499,  "base_units": 200},
    "Cap":                   {"category": "Apparel",       "base_price":  599,  "base_units": 250},
    "Formal Shirt":          {"category": "Apparel",       "base_price": 1899,  "base_units": 110},
    # Home & Kitchen
    "Air Fryer":             {"category": "Home & Kitchen","base_price": 6999,  "base_units": 85},
    "Coffee Maker":          {"category": "Home & Kitchen","base_price": 4299,  "base_units": 100},
    "Blender":               {"category": "Home & Kitchen","base_price": 2799,  "base_units": 120},
    "Non-stick Pan Set":     {"category": "Home & Kitchen","base_price": 1899,  "base_units": 145},
    "Water Bottle":          {"category": "Home & Kitchen","base_price":  699,  "base_units": 320},
    # Books & Stationery
    "Notebook Pack":         {"category": "Books & Stationery","base_price": 499,  "base_units": 380},
    "Fountain Pen":          {"category": "Books & Stationery","base_price": 899,  "base_units": 140},
    "Planner 2025":          {"category": "Books & Stationery","base_price": 699,  "base_units": 220},
    "Sketch Set":            {"category": "Books & Stationery","base_price":1199,  "base_units": 110},
    # Sports & Fitness
    "Resistance Bands":      {"category": "Sports",        "base_price":  799,  "base_units": 290},
    "Yoga Mat":              {"category": "Sports",        "base_price": 1499,  "base_units": 210},
    "Dumbbell Set":          {"category": "Sports",        "base_price": 3999,  "base_units": 80},
    "Protein Powder":        {"category": "Sports",        "base_price": 2499,  "base_units": 150},
}

MONTHS = [f"2024-{m:02d}" for m in range(1, 13)]
REGIONS = ["North", "South", "East", "West", "Central"]

# Seasonal multipliers per category per month
SEASON = {
    "Electronics":      [0.85,0.80,0.90,0.95,1.00,1.05,1.10,1.05,1.10,1.15,1.30,1.45],
    "Apparel":          [1.10,1.00,1.20,1.10,1.00,0.90,0.85,0.90,1.10,1.20,1.30,1.40],
    "Home & Kitchen":   [0.90,0.85,1.00,1.05,1.10,1.00,0.95,1.00,1.10,1.15,1.25,1.35],
    "Books & Stationery":[1.10,1.05,1.00,0.90,0.95,0.90,0.85,1.20,1.15,1.00,1.05,1.10],
    "Sports":           [0.90,0.95,1.10,1.20,1.25,1.15,1.10,1.10,1.05,1.00,0.95,0.90],
}

records = []
for month_idx, month in enumerate(MONTHS):
    for product, info in PRODUCTS.items():
        cat  = info["category"]
        base = info["base_units"]
        seas = SEASON[cat][month_idx]
        for region in REGIONS:
            region_mult = {"North":1.05,"South":0.95,"East":1.10,"West":1.00,"Central":0.90}[region]
            units = int(base * seas * region_mult * np.random.uniform(0.85, 1.15))
            price = info["base_price"] * np.random.uniform(0.96, 1.04)
            discount = np.random.choice([0, 5, 10, 15, 20], p=[0.40,0.25,0.20,0.10,0.05])
            net_price = price * (1 - discount / 100)
            revenue  = round(units * net_price, 2)
            records.append({
                "Month": month,
                "Product": product,
                "Category": cat,
                "Region": region,
                "Units_Sold": units,
                "Unit_Price": round(price, 2),
                "Discount_Pct": discount,
                "Net_Price": round(net_price, 2),
                "Revenue": revenue,
                "Profit_Margin_Pct": round(np.random.uniform(18, 38), 2),
            })

df = pd.DataFrame(records)
df["Profit"] = (df["Revenue"] * df["Profit_Margin_Pct"] / 100).round(2)
df["Month_Num"] = df["Month"].apply(lambda x: int(x.split("-")[1]))
df["Quarter"] = df["Month_Num"].apply(lambda m: f"Q{(m-1)//3+1}")

os.makedirs("output", exist_ok=True)
df.to_csv("data/sales_data.csv", index=False)
print(f"✅ Dataset generated: {len(df):,} records  |  {df['Revenue'].sum()/1e7:.2f} Cr total revenue")
print(df.head(3).to_string())
