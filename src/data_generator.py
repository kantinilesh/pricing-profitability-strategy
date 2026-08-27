"""
Synthetic Data Generation Engine for OmniRetail India.
Generates realistic Indian omnichannel retail datasets with embedded business anomalies,
margin leakages, price elasticities, and customer profitability patterns.
Deterministic generation using fixed seed (seed=42).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def generate_products():
    categories = {
        "Consumer Electronics": {
            "subcategories": ["Smartphones", "Audio & Headphones", "Laptops & Tablets", "Wearables"],
            "price_range": (1500, 75000),
            "margin_range": (0.12, 0.22),
            "brands": ["TechMax", "SonicX", "VoltDevices", "AuraGadgets", "KritiTech"]
        },
        "Apparel & Fashion": {
            "subcategories": ["Ethnic Wear", "Western Wear", "Footwear", "Fashion Accessories"],
            "price_range": (499, 5999),
            "margin_range": (0.45, 0.65),
            "brands": ["VedaStyles", "UrbanWeave", "MetroTreads", "RoyaleFashions", "IndiStyle"]
        },
        "Home & Kitchen": {
            "subcategories": ["Small Appliances", "Cookware & Dining", "Home Decor", "Storage Solutions"],
            "price_range": (799, 14999),
            "margin_range": (0.32, 0.48),
            "brands": ["ChefCraft", "LivingSpace", "PureHome", "HomeComfort", "SmartLiving"]
        },
        "FMCG & Personal Care": {
            "subcategories": ["Skincare & Grooming", "Packaged Foods", "Beverages", "Home Hygiene"],
            "price_range": (99, 1499),
            "margin_range": (0.20, 0.35),
            "brands": ["NurtureNature", "FreshBite", "CleanGlow", "AromaEssence", "VitalFoods"]
        }
    }

    products = []
    sku_id = 1001

    for cat_name, cat_data in categories.items():
        for subcat in cat_data["subcategories"]:
            for brand in cat_data["brands"]:
                for i in range(1, 4):  # 3 SKUs per brand-subcat combo
                    list_price = int(np.random.uniform(*cat_data["price_range"]))
                    # Round list price to standard retail price ending (.99 or 00)
                    list_price = round(list_price, -1) - 1 if list_price > 500 else list_price
                    margin_pct = np.random.uniform(*cat_data["margin_range"])
                    base_cogs = round(list_price * (1 - margin_pct), 2)
                    weight_kg = round(np.random.uniform(0.2, 5.5), 2) if cat_name != "FMCG & Personal Care" else round(np.random.uniform(0.1, 1.0), 2)
                    
                    # Elasticity assignment (Electronics elastic, FMCG inelastic)
                    if cat_name == "Consumer Electronics":
                        elasticity = round(np.random.uniform(-2.2, -1.4), 2)
                    elif cat_name == "Apparel & Fashion":
                        elasticity = round(np.random.uniform(-1.8, -1.1), 2)
                    elif cat_name == "Home & Kitchen":
                        elasticity = round(np.random.uniform(-1.2, -0.6), 2) # underpriced/inelastic
                    else:
                        elasticity = round(np.random.uniform(-0.9, -0.4), 2)

                    products.append({
                        "product_id": f"PROD_{sku_id}",
                        "sku_code": f"SKU-{cat_name[:3].upper()}-{subcat[:3].upper()}-{sku_id}",
                        "product_name": f"{brand} {subcat[:-1] if subcat.endswith('s') else subcat} V{i}",
                        "category": cat_name,
                        "subcategory": subcat,
                        "brand": brand,
                        "list_price_inr": list_price,
                        "base_cogs_inr": base_cogs,
                        "weight_kg": weight_kg,
                        "price_elasticity_target": elasticity,
                        "is_active": True
                    })
                    sku_id += 1

    return pd.DataFrame(products)

def generate_customers(n=500):
    customer_types = ["B2B Enterprise", "B2B SMB", "Retail Platinum", "Retail Gold", "Retail Silver", "Retail Standard"]
    weights = [0.05, 0.10, 0.10, 0.20, 0.25, 0.30]
    regions = ["North", "South", "East", "West"]
    city_tiers = ["Tier 1", "Tier 2", "Tier 3"]

    customers = []
    for i in range(1, n + 1):
        c_type = np.random.choice(customer_types, p=weights)
        region = np.random.choice(regions)
        city_tier = np.random.choice(city_tiers, p=[0.45, 0.35, 0.20])
        
        # Contract discount: B2B Enterprise gets high legacy contract discount
        if c_type == "B2B Enterprise":
            contract_discount_pct = round(np.random.uniform(0.15, 0.25), 3) # Potential dilution
        elif c_type == "B2B SMB":
            contract_discount_pct = round(np.random.uniform(0.08, 0.14), 3)
        elif c_type == "Retail Platinum":
            contract_discount_pct = round(np.random.uniform(0.05, 0.08), 3)
        else:
            contract_discount_pct = 0.0

        join_date = datetime(2022, 1, 1) + timedelta(days=int(np.random.randint(0, 730)))

        customers.append({
            "customer_id": f"CUST_{i:05d}",
            "customer_name": f"Client Account {i:04d}",
            "customer_type": c_type,
            "region": region,
            "city_tier": city_tier,
            "contract_discount_pct": contract_discount_pct,
            "join_date": join_date.strftime("%Y-%m-%d")
        })

    return pd.DataFrame(customers)

def generate_stores():
    regions = ["North", "South", "East", "West"]
    city_tiers = ["Tier 1", "Tier 2", "Tier 3"]
    stores = []
    
    # E-Commerce Channels
    stores.append({
        "store_id": "STORE_ONLINE_DIRECT",
        "store_name": "OmniRetail Direct App & Web",
        "channel": "E-Commerce Direct",
        "region": "National",
        "city_tier": "National",
        "fulfillment_cost_base_pct": 0.08  # 8% of revenue base
    })
    stores.append({
        "store_id": "STORE_ONLINE_MARKETPLACE",
        "store_name": "Marketplace Partners (Amazon/Flipkart)",
        "channel": "E-Commerce Marketplace",
        "region": "National",
        "city_tier": "National",
        "fulfillment_cost_base_pct": 0.12  # 12% marketplace fee
    })

    # Physical Stores across India
    store_num = 1
    for region in regions:
        for tier in city_tiers:
            count = 4 if tier == "Tier 1" else (3 if tier == "Tier 2" else 2)
            for _ in range(count):
                stores.append({
                    "store_id": f"STORE_PHY_{store_num:03d}",
                    "store_name": f"OmniRetail Store {store_num} ({region} - {tier})",
                    "channel": "Physical Store",
                    "region": region,
                    "city_tier": tier,
                    "fulfillment_cost_base_pct": 0.03 if tier == "Tier 1" else (0.04 if tier == "Tier 2" else 0.06)
                })
                store_num += 1

    return pd.DataFrame(stores)

def generate_promotions():
    promotions = [
        {"promo_id": "PROMO_NONE", "promo_name": "No Promotion / Baseline", "promo_type": "None", "discount_pct": 0.0, "vendor_coop_funding_pct": 0.0},
        {"promo_id": "PROMO_DIWALI", "promo_name": "Diwali Festive Dhamaka", "promo_type": "Festive Campaign", "discount_pct": 0.20, "vendor_coop_funding_pct": 0.30},
        {"promo_id": "PROMO_NAVRATRI", "promo_name": "Navratri Festive Special", "promo_type": "Festive Campaign", "discount_pct": 0.15, "vendor_coop_funding_pct": 0.20},
        {"promo_id": "PROMO_EOSS", "promo_name": "End of Season Sale (EOSS)", "promo_type": "Clearance Markdown", "discount_pct": 0.30, "vendor_coop_funding_pct": 0.10}, # Negative ROI potential
        {"promo_id": "PROMO_FLASH_WED", "promo_name": "E-Comm Flash Wednesday", "promo_type": "Digital Flash", "discount_pct": 0.12, "vendor_coop_funding_pct": 0.50},
        {"promo_id": "PROMO_BULK_B2B", "promo_name": "B2B Volume Incentive", "promo_type": "Trade Promo", "discount_pct": 0.10, "vendor_coop_funding_pct": 0.00}
    ]
    return pd.DataFrame(promotions)

def generate_transactions(products_df, customers_df, stores_df, promotions_df, n_transactions=15000):
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days

    tx_list = []

    # Map fast lookups
    prod_dict = products_df.set_index("product_id").to_dict("index")
    cust_dict = customers_df.set_index("customer_id").to_dict("index")
    store_dict = stores_df.set_index("store_id").to_dict("index")
    promo_dict = promotions_df.set_index("promo_id").to_dict("index")

    p_ids = products_df["product_id"].values
    c_ids = customers_df["customer_id"].values
    s_ids = stores_df["store_id"].values
    pr_ids = promotions_df["promo_id"].values

    for i in range(1, n_transactions + 1):
        # Random Date with Festive Seasonality (Oct-Nov Diwali spike)
        day_offset = int(np.random.randint(0, total_days))
        tx_date = start_date + timedelta(days=day_offset)
        month = tx_date.month

        # Assign promotion based on month
        if month in [10, 11] and np.random.rand() < 0.6:
            promo_id = "PROMO_DIWALI" if np.random.rand() < 0.7 else "PROMO_NAVRATRI"
        elif month in [1, 7] and np.random.rand() < 0.5:
            promo_id = "PROMO_EOSS"
        elif np.random.rand() < 0.2:
            promo_id = "PROMO_FLASH_WED"
        else:
            promo_id = "PROMO_NONE"

        cust_id = np.random.choice(c_ids)
        prod_id = np.random.choice(p_ids)
        store_id = np.random.choice(s_ids)

        c_info = cust_dict[cust_id]
        p_info = prod_dict[prod_id]
        s_info = store_dict[store_id]
        pr_info = promo_dict[promo_id]

        # Quantity depends on Customer Type
        if c_info["customer_type"] in ["B2B Enterprise", "B2B SMB"]:
            qty = int(np.random.randint(10, 150))
        else:
            qty = int(np.random.randint(1, 5))

        list_price = p_info["list_price_inr"]
        gross_rev = round(list_price * qty, 2)

        # Off-invoice & Contract Discounts
        contract_disc_pct = c_info["contract_discount_pct"]
        promo_disc_pct = pr_info["discount_pct"]

        # Ad-hoc discretionary discount leakage (embedded anomaly in E-Commerce & Tier 3)
        adhoc_disc_pct = 0.0
        if s_info["channel"] in ["E-Commerce Direct", "E-Commerce Marketplace"] and p_info["category"] in ["Consumer Electronics", "Apparel & Fashion"]:
            if np.random.rand() < 0.35:
                adhoc_disc_pct = round(np.random.uniform(0.04, 0.12), 3) # Unplanned markdown leakage

        total_discount_pct = min(0.50, contract_disc_pct + promo_disc_pct + adhoc_disc_pct)
        total_discount_inr = round(gross_rev * total_discount_pct, 2)
        net_rev = round(gross_rev - total_discount_inr, 2)

        # COGS
        cogs_inr = round(p_info["base_cogs_inr"] * qty, 2)

        # Logistics & Fulfillment Cost (Cost-to-Serve)
        # Tier 3 & E-Commerce have higher shipping costs
        base_logistics_rate = s_info["fulfillment_cost_base_pct"]
        if c_info["city_tier"] == "Tier 3" and s_info["channel"].startswith("E-Commerce"):
            logistics_multiplier = 1.65 # Logistics cost overrun in Tier 3 e-commerce
        elif c_info["city_tier"] == "Tier 2" and s_info["channel"].startswith("E-Commerce"):
            logistics_multiplier = 1.25
        else:
            logistics_multiplier = 1.00

        fulfillment_cost_inr = round(net_rev * base_logistics_rate * logistics_multiplier + (qty * p_info["weight_kg"] * 15.0), 2)

        # Promo Vendor Funding offset
        vendor_coop_inr = round(total_discount_inr * pr_info["vendor_coop_funding_pct"], 2)
        net_promo_cost_inr = round((gross_rev * promo_disc_pct) - vendor_coop_inr, 2)

        # Returns logic (Apparel e-commerce has ~18% return rate)
        return_flag = False
        return_cost_inr = 0.0
        if s_info["channel"].startswith("E-Commerce") and p_info["category"] == "Apparel & Fashion":
            if np.random.rand() < 0.18:
                return_flag = True
                return_cost_inr = round(fulfillment_cost_inr * 0.8 + 150.0, 2) # Reverse logistics + repackaging
        elif s_info["channel"].startswith("E-Commerce"):
            if np.random.rand() < 0.06:
                return_flag = True
                return_cost_inr = round(fulfillment_cost_inr * 0.7 + 100.0, 2)

        # Pocket Profit (Net margin after all leakages)
        pocket_profit_inr = round(net_rev - cogs_inr - fulfillment_cost_inr - return_cost_inr + vendor_coop_inr, 2)

        tx_list.append({
            "transaction_id": f"TX_{i:07d}",
            "transaction_date": tx_date.strftime("%Y-%m-%d"),
            "customer_id": cust_id,
            "store_id": store_id,
            "product_id": prod_id,
            "promo_id": promo_id,
            "channel": s_info["channel"],
            "region": c_info["region"],
            "city_tier": c_info["city_tier"],
            "quantity": qty,
            "list_price_inr": list_price,
            "gross_revenue_inr": gross_rev,
            "contract_discount_inr": round(gross_rev * contract_disc_pct, 2),
            "promo_discount_inr": round(gross_rev * promo_disc_pct, 2),
            "adhoc_discount_inr": round(gross_rev * adhoc_disc_pct, 2),
            "total_discount_inr": total_discount_inr,
            "net_revenue_inr": net_rev,
            "base_cogs_inr": cogs_inr,
            "fulfillment_cost_inr": fulfillment_cost_inr,
            "vendor_coop_rebate_inr": vendor_coop_inr,
            "return_flag": return_flag,
            "return_cost_inr": return_cost_inr,
            "pocket_profit_inr": pocket_profit_inr
        })

    return pd.DataFrame(tx_list)

def generate_competitor_benchmarks(products_df):
    competitors = ["Reliance Retail", "D-Mart", "Amazon India", "Flipkart"]
    benchmarks = []
    
    obs_date = "2025-12-01"
    for _, row in products_df.iterrows():
        p_id = row["product_id"]
        l_price = row["list_price_inr"]
        cat = row["category"]
        
        for comp in competitors:
            # Home & Kitchen SKUs priced higher by competitors (underpriced OmniRetail SKUs)
            if cat == "Home & Kitchen":
                price_ratio = np.random.uniform(1.05, 1.18)
            elif cat == "Consumer Electronics":
                price_ratio = np.random.uniform(0.95, 1.03)
            else:
                price_ratio = np.random.uniform(0.97, 1.06)

            comp_price = round(l_price * price_ratio, 2)
            benchmarks.append({
                "observation_date": obs_date,
                "product_id": p_id,
                "competitor_name": comp,
                "competitor_price_inr": comp_price,
                "omniretail_list_price_inr": l_price,
                "price_index_vs_competitor": round(l_price / comp_price, 3)
            })

    return pd.DataFrame(benchmarks)

def main():
    set_seed(42)
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Master Data Tables for OmniRetail India...")
    df_products = generate_products()
    df_customers = generate_customers(n=500)
    df_stores = generate_stores()
    df_promotions = generate_promotions()
    
    print("Generating Transactional Dataset (~15,000 transactions)...")
    df_transactions = generate_transactions(df_products, df_customers, df_stores, df_promotions, n_transactions=15000)

    print("Generating Competitor Benchmarks...")
    df_competitors = generate_competitor_benchmarks(df_products)

    # Save to data/raw/
    df_products.to_csv(os.path.join(output_dir, "dim_products.csv"), index=False)
    df_customers.to_csv(os.path.join(output_dir, "dim_customers.csv"), index=False)
    df_stores.to_csv(os.path.join(output_dir, "dim_stores.csv"), index=False)
    df_promotions.to_csv(os.path.join(output_dir, "dim_promotions.csv"), index=False)
    df_transactions.to_csv(os.path.join(output_dir, "fact_transactions.csv"), index=False)
    df_competitors.to_csv(os.path.join(output_dir, "fact_competitor_prices.csv"), index=False)

    print(f"Data Generation Complete. Saved all raw CSVs in: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()
