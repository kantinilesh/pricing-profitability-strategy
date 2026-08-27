"""
04_build_analytical_dataset.py
Joins cleaned transaction records with master dimension tables (calendar, customers, products,
regions, channels, promotions) to construct the primary analytical dataset data mart.
Outputs data/processed/analytical_dataset.csv.
"""

import os
import duckdb
import pandas as pd

def build_analytical_dataset(raw_dir, processed_dir):
    os.makedirs(processed_dir, exist_ok=True)
    con = duckdb.connect(database=":memory:")

    print("Loading cleaned transaction data and dimensions into DuckDB engine...")
    con.execute(f"CREATE TABLE transactions_cleaned AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'transactions_cleaned.csv')}')")
    con.execute(f"CREATE TABLE calendar AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'calendar.csv')}')")
    con.execute(f"CREATE TABLE customers AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'customers.csv')}')")
    con.execute(f"CREATE TABLE products AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'products.csv')}')")
    con.execute(f"CREATE TABLE regions AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'regions.csv')}')")
    con.execute(f"CREATE TABLE channels AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'channels.csv')}')")
    con.execute(f"CREATE TABLE promotions AS SELECT * FROM read_csv_auto('{os.path.join(raw_dir, 'promotions.csv')}')")

    query = """
    CREATE TABLE analytical_mart AS
    SELECT 
        t.transaction_id,
        t.date,
        cal.year,
        cal.quarter,
        cal.month,
        cal.month_name,
        cal.day_of_week,
        cal.is_weekend,
        cal.is_festive_season,
        t.customer_id,
        c.customer_name,
        t.customer_segment,
        c.contract_discount_pct,
        t.product_id,
        p.product_name,
        t.category,
        p.subcategory,
        t.region,
        r.primary_hub,
        r.logistics_cost_tier,
        t.channel,
        ch.take_rate_pct,
        ch.cost_to_serve_base_pct,
        t.units,
        t.list_price,
        t.selling_price,
        t.discount,
        t.discount_pct,
        t.revenue,
        t.variable_cost,
        t.gross_profit,
        ROUND((t.gross_profit / NULLIF(t.revenue, 0)) * 100, 2) AS gross_margin_pct,
        t.promotion_flag,
        t.promotion_type,
        pr.vendor_coop_share_pct,
        t.is_outlier
    FROM transactions_cleaned t
    LEFT JOIN calendar cal ON t.date = cal.date
    LEFT JOIN customers c ON t.customer_id = c.customer_id
    LEFT JOIN products p ON t.product_id = p.product_id
    LEFT JOIN regions r ON t.region = r.region
    LEFT JOIN channels ch ON t.channel = ch.channel
    LEFT JOIN promotions pr ON t.promotion_type = pr.promotion_type
    """
    con.execute(query)
    df_mart = con.execute("SELECT * FROM analytical_mart").df()

    out_path = os.path.join(processed_dir, "analytical_dataset.csv")
    df_mart.to_csv(out_path, index=False)

    # Save cleaned supporting dimension tables to data/processed/
    con.execute(f"COPY customers TO '{os.path.join(processed_dir, 'dim_customers.csv')}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY products TO '{os.path.join(processed_dir, 'dim_products.csv')}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY regions TO '{os.path.join(processed_dir, 'dim_regions.csv')}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY channels TO '{os.path.join(processed_dir, 'dim_channels.csv')}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY promotions TO '{os.path.join(processed_dir, 'dim_promotions.csv')}' (HEADER, DELIMITER ',')")
    con.execute(f"COPY calendar TO '{os.path.join(processed_dir, 'dim_calendar.csv')}' (HEADER, DELIMITER ',')")

    print(f"Analytical Dataset Mart successfully created: {out_path} ({len(df_mart):,} records)")

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
    processed_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
    build_analytical_dataset(raw_dir, processed_dir)

if __name__ == "__main__":
    main()
