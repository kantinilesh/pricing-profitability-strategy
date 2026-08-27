"""
Data Mart Builder & ETL Engine.
Joins raw transaction facts with master dimension tables and generates aggregated 
analytical data marts for Profitability, Pricing, Customer Whale Curve, and Promo Lift analyses.
"""

import os
import duckdb
import pandas as pd

def build_analytical_marts(raw_dir, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    con = duckdb.connect(database=":memory:")

    print("Loading raw datasets into DuckDB engine...")
    con.execute(f"CREATE TABLE dim_products AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'dim_products.csv')}')")
    con.execute(f"CREATE TABLE dim_customers AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'dim_customers.csv')}')")
    con.execute(f"CREATE TABLE dim_stores AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'dim_stores.csv')}')")
    con.execute(f"CREATE TABLE dim_promotions AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'dim_promotions.csv')}')")
    con.execute(f"CREATE TABLE fact_tx AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'fact_transactions.csv')}')")
    con.execute(f"CREATE TABLE fact_comp AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'fact_competitor_prices.csv')}')")

    # 1. Joined Fact Transaction Mart
    print("Building analytical_transaction_fact dataset...")
    query_fact = """
    CREATE TABLE transaction_fact_mart AS
    SELECT 
        t.transaction_id,
        t.transaction_date,
        t.customer_id,
        c.customer_name,
        c.customer_type,
        c.contract_discount_pct,
        t.store_id,
        s.store_name,
        t.channel,
        t.region,
        t.city_tier,
        t.product_id,
        p.sku_code,
        p.product_name,
        p.category,
        p.subcategory,
        p.brand,
        t.promo_id,
        pr.promo_name,
        pr.promo_type,
        t.quantity,
        t.list_price_inr,
        t.gross_revenue_inr,
        t.contract_discount_inr,
        t.promo_discount_inr,
        t.adhoc_discount_inr,
        t.total_discount_inr,
        t.net_revenue_inr,
        t.base_cogs_inr,
        (t.net_revenue_inr - t.base_cogs_inr) AS gross_margin_inr,
        ROUND((t.net_revenue_inr - t.base_cogs_inr) / NULLIF(t.net_revenue_inr, 0) * 100, 2) AS gross_margin_pct,
        t.fulfillment_cost_inr,
        t.vendor_coop_rebate_inr,
        t.return_flag,
        t.return_cost_inr,
        t.pocket_profit_inr,
        ROUND(t.pocket_profit_inr / NULLIF(t.net_revenue_inr, 0) * 100, 2) AS pocket_margin_pct,
        ROUND((t.total_discount_inr / NULLIF(t.gross_revenue_inr, 0)) * 100, 2) AS discount_waterfall_pct
    FROM fact_tx t
    LEFT JOIN dim_products p ON t.product_id = p.product_id
    LEFT JOIN dim_customers c ON t.customer_id = c.customer_id
    LEFT JOIN dim_stores s ON t.store_id = s.store_id
    LEFT JOIN dim_promotions pr ON t.promo_id = pr.promo_id
    """
    con.execute(query_fact)
    df_fact = con.execute("SELECT * FROM transaction_fact_mart").df()
    df_fact.to_csv(os.path.join(processed_dir, "analytical_transaction_fact.csv"), index=False)

    # 2. Product Margin Mart
    print("Building product_margin_mart dataset...")
    query_prod = """
    SELECT 
        p.product_id,
        p.sku_code,
        p.product_name,
        p.category,
        p.subcategory,
        p.brand,
        p.list_price_inr,
        p.base_cogs_inr,
        p.price_elasticity_target,
        SUM(t.quantity) AS total_units_sold,
        SUM(t.gross_revenue_inr) AS total_gross_revenue_inr,
        SUM(t.total_discount_inr) AS total_discount_inr,
        SUM(t.net_revenue_inr) AS total_net_revenue_inr,
        SUM(t.base_cogs_inr) AS total_cogs_inr,
        SUM(t.gross_margin_inr) AS total_gross_margin_inr,
        ROUND(SUM(t.gross_margin_inr) / NULLIF(SUM(t.net_revenue_inr), 0) * 100, 2) AS avg_gross_margin_pct,
        SUM(t.fulfillment_cost_inr) AS total_fulfillment_cost_inr,
        SUM(t.return_cost_inr) AS total_return_cost_inr,
        SUM(t.pocket_profit_inr) AS total_pocket_profit_inr,
        ROUND(SUM(t.pocket_profit_inr) / NULLIF(SUM(t.net_revenue_inr), 0) * 100, 2) AS avg_pocket_margin_pct,
        ROUND(AVG(t.discount_waterfall_pct), 2) AS avg_discount_waterfall_pct,
        ROUND(AVG(comp.price_index_vs_competitor), 3) AS avg_competitor_price_index
    FROM dim_products p
    LEFT JOIN transaction_fact_mart t ON p.product_id = t.product_id
    LEFT JOIN (
        SELECT product_id, AVG(price_index_vs_competitor) AS price_index_vs_competitor 
        FROM fact_comp GROUP BY product_id
    ) comp ON p.product_id = comp.product_id
    GROUP BY p.product_id, p.sku_code, p.product_name, p.category, p.subcategory, p.brand, p.list_price_inr, p.base_cogs_inr, p.price_elasticity_target
    ORDER BY total_net_revenue_inr DESC
    """
    df_prod = con.execute(query_prod).df()
    df_prod.to_csv(os.path.join(processed_dir, "product_margin_mart.csv"), index=False)

    # 3. Customer Profitability Mart
    print("Building customer_profitability_mart dataset...")
    query_cust = """
    SELECT 
        c.customer_id,
        c.customer_name,
        c.customer_type,
        c.region,
        c.city_tier,
        c.contract_discount_pct,
        COUNT(DISTINCT t.transaction_id) AS total_orders,
        SUM(t.quantity) AS total_units_purchased,
        SUM(t.gross_revenue_inr) AS total_gross_revenue_inr,
        SUM(t.total_discount_inr) AS total_discount_inr,
        SUM(t.net_revenue_inr) AS total_net_revenue_inr,
        SUM(t.base_cogs_inr) AS total_cogs_inr,
        SUM(t.fulfillment_cost_inr) AS total_fulfillment_cost_inr,
        SUM(t.pocket_profit_inr) AS total_pocket_profit_inr,
        ROUND(SUM(t.pocket_profit_inr) / NULLIF(SUM(t.net_revenue_inr), 0) * 100, 2) AS customer_pocket_margin_pct
    FROM dim_customers c
    LEFT JOIN transaction_fact_mart t ON c.customer_id = t.customer_id
    GROUP BY c.customer_id, c.customer_name, c.customer_type, c.region, c.city_tier, c.contract_discount_pct
    ORDER BY total_pocket_profit_inr DESC
    """
    df_cust = con.execute(query_cust).df()
    df_cust.to_csv(os.path.join(processed_dir, "customer_profitability_mart.csv"), index=False)

    # 4. Promo Performance Mart
    print("Building promo_performance_mart dataset...")
    query_promo = """
    SELECT 
        pr.promo_id,
        pr.promo_name,
        pr.promo_type,
        COUNT(t.transaction_id) AS transaction_count,
        SUM(t.quantity) AS total_units_sold,
        SUM(t.gross_revenue_inr) AS total_gross_revenue_inr,
        SUM(t.promo_discount_inr) AS total_promo_spend_inr,
        SUM(t.vendor_coop_rebate_inr) AS total_vendor_coop_inr,
        SUM(t.net_revenue_inr) AS total_net_revenue_inr,
        SUM(t.pocket_profit_inr) AS total_pocket_profit_inr,
        ROUND(SUM(t.pocket_profit_inr) / NULLIF(SUM(t.net_revenue_inr), 0) * 100, 2) AS promo_pocket_margin_pct
    FROM dim_promotions pr
    LEFT JOIN transaction_fact_mart t ON pr.promo_id = t.promo_id
    GROUP BY pr.promo_id, pr.promo_name, pr.promo_type
    ORDER BY total_net_revenue_inr DESC
    """
    df_promo = con.execute(query_promo).df()
    df_promo.to_csv(os.path.join(processed_dir, "promo_performance_mart.csv"), index=False)

    # 5. Channel & Region Mart
    print("Building channel_region_mart dataset...")
    query_cr = """
    SELECT 
        channel,
        region,
        city_tier,
        COUNT(transaction_id) AS order_count,
        SUM(net_revenue_inr) AS total_net_revenue_inr,
        SUM(total_discount_inr) AS total_discount_inr,
        SUM(fulfillment_cost_inr) AS total_fulfillment_cost_inr,
        ROUND(SUM(fulfillment_cost_inr) / NULLIF(SUM(net_revenue_inr), 0) * 100, 2) AS fulfillment_cost_pct,
        SUM(CASE WHEN return_flag THEN 1 ELSE 0 END) AS return_count,
        ROUND(SUM(CASE WHEN return_flag THEN 1 ELSE 0 END) * 100.0 / COUNT(transaction_id), 2) AS return_rate_pct,
        SUM(pocket_profit_inr) AS total_pocket_profit_inr,
        ROUND(SUM(pocket_profit_inr) / NULLIF(SUM(net_revenue_inr), 0) * 100, 2) AS pocket_margin_pct
    FROM transaction_fact_mart
    GROUP BY channel, region, city_tier
    ORDER BY channel, region, city_tier
    """
    df_cr = con.execute(query_cr).df()
    df_cr.to_csv(os.path.join(processed_dir, "channel_region_mart.csv"), index=False)

    print("ETL & Data Mart Generation Completed Successfully!")

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    build_analytical_marts(raw_dir, processed_dir)

if __name__ == "__main__":
    main()
