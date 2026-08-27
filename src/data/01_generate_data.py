"""
01_generate_data.py
Generates a realistic synthetic Indian retail dataset for OmniRetail India (~60,000 transaction records,
750 customers, 75 products, 6 regions, 4 channels, 24 months history) with controlled, documented data-quality issues.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def generate_calendar():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    calendar = []
    for d in date_list:
        month = d.month
        is_festive = 1 if month in [10, 11] else 0  # Oct-Nov Diwali/Navratri
        calendar.append({
            "date": d.strftime("%Y-%m-%d"),
            "year": d.year,
            "quarter": f"Q{(month - 1) // 3 + 1}",
            "month": month,
            "month_name": d.strftime("%B"),
            "day": d.day,
            "day_of_week": d.strftime("%A"),
            "is_weekend": 1 if d.weekday() >= 5 else 0,
            "is_festive_season": is_festive
        })
    return pd.DataFrame(calendar)

def generate_regions():
    return pd.DataFrame([
        {"region_id": "REG_NORTH", "region": "North", "primary_hub": "Delhi NCR", "logistics_cost_tier": "Standard"},
        {"region_id": "REG_SOUTH", "region": "South", "primary_hub": "Bengaluru", "logistics_cost_tier": "Standard"},
        {"region_id": "REG_WEST", "region": "West", "primary_hub": "Mumbai", "logistics_cost_tier": "Standard"},
        {"region_id": "REG_EAST", "region": "East", "primary_hub": "Kolkata", "logistics_cost_tier": "Medium"},
        {"region_id": "REG_CENTRAL", "region": "Central", "primary_hub": "Indore", "logistics_cost_tier": "Medium"},
        {"region_id": "REG_NORTHEAST", "region": "North-East", "primary_hub": "Guwahati", "logistics_cost_tier": "High"}
    ])

def generate_channels():
    return pd.DataFrame([
        {"channel_id": "CHN_STORE", "channel": "Physical Retail Store", "take_rate_pct": 0.0, "cost_to_serve_base_pct": 0.04},
        {"channel_id": "CHN_DIRECT", "channel": "E-Commerce Direct", "take_rate_pct": 0.0, "cost_to_serve_base_pct": 0.08},
        {"channel_id": "CHN_MKT", "channel": "E-Commerce Marketplace", "take_rate_pct": 0.10, "cost_to_serve_base_pct": 0.12},
        {"channel_id": "CHN_QUICK", "channel": "Quick-Commerce", "take_rate_pct": 0.05, "cost_to_serve_base_pct": 0.15}
    ])

def generate_promotions():
    return pd.DataFrame([
        {"promo_id": "PRM_NONE", "promotion_type": "Baseline / None", "default_discount_pct": 0.0, "vendor_coop_share_pct": 0.0},
        {"promo_id": "PRM_DIWALI", "promotion_type": "Festive Dhamaka", "default_discount_pct": 0.20, "vendor_coop_share_pct": 0.35},
        {"promo_id": "PRM_NAVRATRI", "promotion_type": "Navratri Special", "default_discount_pct": 0.15, "vendor_coop_share_pct": 0.25},
        {"promo_id": "PRM_EOSS", "promotion_type": "EOSS Clearance", "default_discount_pct": 0.30, "vendor_coop_share_pct": 0.10},
        {"promo_id": "PRM_FLASH", "promotion_type": "Flash Wednesday", "default_discount_pct": 0.12, "vendor_coop_share_pct": 0.40},
        {"promo_id": "PRM_BULK", "promotion_type": "B2B Volume Incentive", "default_discount_pct": 0.10, "vendor_coop_share_pct": 0.00}
    ])

def generate_products():
    categories = [
        ("Consumer Electronics", 15, (2500, 65000), (0.12, 0.22)),
        ("Apparel & Fashion", 15, (599, 4999), (0.45, 0.65)),
        ("Home & Kitchen", 15, (899, 12999), (0.32, 0.48)),
        ("FMCG & Personal Care", 10, (149, 1299), (0.20, 0.35)),
        ("Footwear", 10, (799, 5999), (0.40, 0.58)),
        ("Beauty & Cosmetics", 10, (299, 3499), (0.50, 0.70))
    ]

    products = []
    p_idx = 101

    for cat_name, count, price_range, margin_range in categories:
        for i in range(1, count + 1):
            l_price = float(np.random.uniform(*price_range))
            l_price = round(l_price, -1) - 1.0 if l_price > 500 else round(l_price, 2)
            margin = np.random.uniform(*margin_range)
            base_cogs = round(l_price * (1.0 - margin), 2)
            
            products.append({
                "product_id": f"PRD_{p_idx}",
                "product_name": f"{cat_name.split()[0]} Item {i}",
                "category": cat_name,
                "subcategory": f"{cat_name.split()[0]} Sub {((i-1)%3)+1}",
                "list_price": l_price,
                "unit_cogs": base_cogs
            })
            p_idx += 1

    return pd.DataFrame(products)

def generate_customers(n=750):
    segments = ["B2B Enterprise", "B2B SMB", "Retail Platinum", "Retail Gold", "Retail Silver", "Retail Standard"]
    seg_weights = [0.05, 0.10, 0.10, 0.20, 0.25, 0.30]
    regions = ["North", "South", "West", "East", "Central", "North-East"]

    customers = []
    for i in range(1, n + 1):
        seg = np.random.choice(segments, p=seg_weights)
        reg = np.random.choice(regions)
        contract_disc = round(np.random.uniform(0.12, 0.22), 3) if seg == "B2B Enterprise" else (
            round(np.random.uniform(0.06, 0.12), 3) if seg == "B2B SMB" else 0.0
        )

        customers.append({
            "customer_id": f"CST_{i:04d}",
            "customer_name": f"Customer Account {i:04d}",
            "customer_segment": seg,
            "region": reg,
            "contract_discount_pct": contract_disc,
            "created_date": "2023-01-15"
        })

    return pd.DataFrame(customers)

def generate_transactions(products_df, customers_df, regions_df, channels_df, promos_df, calendar_df, n_tx=60000):
    dates = calendar_df["date"].values
    p_records = products_df.to_dict("records")
    c_records = customers_df.to_dict("records")
    r_names = regions_df["region"].values
    ch_names = channels_df["channel"].values
    prm_records = promos_df.to_dict("records")

    tx_data = []

    for i in range(1, n_tx + 1):
        d = np.random.choice(dates)
        month = int(d.split("-")[1])
        
        c_obj = random.choice(c_records)
        p_obj = random.choice(p_records)
        region = c_obj["region"]
        channel = np.random.choice(ch_names, p=[0.45, 0.30, 0.18, 0.07])

        # Promotion determination based on month
        if month in [10, 11] and random.random() < 0.55:
            prm_obj = prm_records[1] if random.random() < 0.7 else prm_records[2]  # Festive / Navratri
        elif month in [1, 7] and random.random() < 0.45:
            prm_obj = prm_records[3]  # EOSS
        elif random.random() < 0.15:
            prm_obj = prm_records[4]  # Flash
        else:
            prm_obj = prm_records[0]  # None

        # Units based on Customer Segment
        if c_obj["customer_segment"] in ["B2B Enterprise", "B2B SMB"]:
            units = int(np.random.randint(10, 120))
        else:
            units = int(np.random.randint(1, 5))

        list_p = p_obj["list_price"]
        unit_cogs = p_obj["unit_cogs"]

        # Discount Calculation
        contract_d = c_obj["contract_discount_pct"]
        promo_d = prm_obj["default_discount_pct"]
        adhoc_d = round(np.random.uniform(0.03, 0.10), 3) if channel.startswith("E-Commerce") and random.random() < 0.25 else 0.0

        tot_disc_pct = min(0.50, contract_d + promo_d + adhoc_d)
        selling_price = round(list_p * (1.0 - tot_disc_pct), 2)
        unit_discount = round(list_p - selling_price, 2)

        # Revenue & Cost Math (Reconciled Base)
        revenue = round(units * selling_price, 2)
        
        # Logistics & Channel Variable Cost
        logistics_rate = 0.05 if channel == "Physical Retail Store" else (0.09 if channel == "E-Commerce Direct" else 0.13)
        var_cost = round((units * unit_cogs) + (revenue * logistics_rate), 2)
        gross_profit = round(revenue - var_cost, 2)

        promo_flag = 1 if prm_obj["promo_id"] != "PRM_NONE" else 0

        tx_data.append({
            "transaction_id": f"TXN_{i:06d}",
            "date": d,
            "customer_id": c_obj["customer_id"],
            "product_id": p_obj["product_id"],
            "category": p_obj["category"],
            "region": region,
            "channel": channel,
            "units": units,
            "list_price": list_p,
            "selling_price": selling_price,
            "discount": unit_discount,
            "discount_pct": round(tot_disc_pct * 100, 2),
            "revenue": revenue,
            "variable_cost": var_cost,
            "gross_profit": gross_profit,
            "promotion_flag": promo_flag,
            "promotion_type": prm_obj["promotion_type"],
            "customer_segment": c_obj["customer_segment"]
        })

    df_tx = pd.DataFrame(tx_data)

    # --- INJECT REALISTIC DATA QUALITY ANOMALIES ---
    print("Injecting controlled realistic data-quality issues...")
    
    # 1. Category Casing/Space Inconsistencies (~2% of rows)
    inconsistent_mask = np.random.rand(len(df_tx)) < 0.02
    df_tx.loc[inconsistent_mask & (df_tx["category"] == "Consumer Electronics"), "category"] = "consumer_electronics"
    df_tx.loc[inconsistent_mask & (df_tx["category"] == "Apparel & Fashion"), "category"] = "Apparel & Fashion  "
    df_tx.loc[inconsistent_mask & (df_tx["category"] == "Home & Kitchen"), "category"] = "home_&_kitchen"

    # 2. Missing Values (~1.2% in customer_segment, variable_cost, promotion_type)
    missing_seg_mask = np.random.rand(len(df_tx)) < 0.012
    df_tx.loc[missing_seg_mask, "customer_segment"] = np.nan
    missing_cost_mask = np.random.rand(len(df_tx)) < 0.008
    df_tx.loc[missing_cost_mask, "variable_cost"] = np.nan

    # 3. Duplicate Records (~0.8% duplicate rows)
    dup_rows = df_tx.sample(n=int(len(df_tx) * 0.008), random_state=42)
    df_tx = pd.concat([df_tx, dup_rows], ignore_index=True)

    # 4. Outliers (~0.3% erroneous high units or list prices)
    outlier_mask = np.random.rand(len(df_tx)) < 0.003
    df_tx.loc[outlier_mask, "units"] = df_tx.loc[outlier_mask, "units"] * 100

    # 5. Invalid / Negative Revenue Keying Errors (~0.15% negative revenue)
    neg_mask = np.random.rand(len(df_tx)) < 0.0015
    df_tx.loc[neg_mask, "revenue"] = -1 * df_tx.loc[neg_mask, "revenue"].abs()

    return df_tx

def main():
    set_seed(42)
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)

    print("Generating Master Dimension Tables...")
    df_cal = generate_calendar()
    df_reg = generate_regions()
    df_chn = generate_channels()
    df_prm = generate_promotions()
    df_prd = generate_products()
    df_cst = generate_customers()

    print("Generating 60,000+ Raw Transaction Records with Controlled Anomalies...")
    df_tx = generate_transactions(df_prd, df_cst, df_reg, df_chn, df_prm, df_cal, n_tx=60000)

    # Save to data/raw/
    df_cal.to_csv(os.path.join(raw_dir, "calendar.csv"), index=False)
    df_reg.to_csv(os.path.join(raw_dir, "regions.csv"), index=False)
    df_chn.to_csv(os.path.join(raw_dir, "channels.csv"), index=False)
    df_prm.to_csv(os.path.join(raw_dir, "promotions.csv"), index=False)
    df_prd.to_csv(os.path.join(raw_dir, "products.csv"), index=False)
    df_cst.to_csv(os.path.join(raw_dir, "customers.csv"), index=False)
    df_tx.to_csv(os.path.join(raw_dir, "transactions_raw.csv"), index=False)

    print(f"Data Generation Complete. Saved all raw CSVs in: {os.path.abspath(raw_dir)}")
    print(f"Raw Transaction Count: {len(df_tx):,} records.")

if __name__ == "__main__":
    main()
