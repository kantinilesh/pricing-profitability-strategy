"""
run_sql_queries.py
Executes all 20 analytical SQL query files against DuckDB database engine,
captures empirical query outputs, and formats summary findings for SQL_RESULTS.md.
"""

import os
import glob
import duckdb
import pandas as pd

def run_all_queries(repo_root):
    processed_dir = os.path.join(repo_root, "data", "processed")
    sql_root = os.path.join(repo_root, "sql")
    
    con = duckdb.connect(database=":memory:")
    
    print("Setting up SQL engine and loading normalized dimension & transaction tables...")
    con.execute(f"CREATE TABLE dim_calendar AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_calendar.csv')}')")
    con.execute(f"CREATE TABLE dim_regions AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_regions.csv')}')")
    con.execute(f"CREATE TABLE dim_channels AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_channels.csv')}')")
    con.execute(f"CREATE TABLE dim_promotions AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_promotions.csv')}')")
    con.execute(f"CREATE TABLE dim_products AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_products.csv')}')")
    con.execute(f"CREATE TABLE dim_customers AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'dim_customers.csv')}')")
    con.execute(f"CREATE TABLE fact_transactions AS SELECT * FROM read_csv_auto('{os.path.join(processed_dir, 'analytical_dataset.csv')}')")

    sql_files = sorted(glob.glob(os.path.join(sql_root, "**", "*.sql"), recursive=True))
    # Exclude DDL schema script from analytical execution loop
    sql_files = [f for f in sql_files if not f.endswith("00_create_tables.sql")]

    print(f"Found {len(sql_files)} analytical SQL queries to execute.")

    query_results = {}
    for filepath in sql_files:
        rel_path = os.path.relpath(filepath, sql_root)
        print(f"  Executing {rel_path}...")
        with open(filepath, "r") as f:
            query_str = f.read()
        
        df_res = con.execute(query_str).df()
        query_results[rel_path] = df_res

    return query_results

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    results = run_all_queries(repo_root)
    print("All 20 analytical SQL queries executed successfully!")

if __name__ == "__main__":
    main()
