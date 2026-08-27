-- ============================================================================
-- PostgreSQL / DuckDB DDL: Normalized Schema Setup
-- Project: Pricing & Profitability Strategy Platform (OmniRetail India)
-- ============================================================================

-- 1. Calendar Dimension
CREATE TABLE IF NOT EXISTS dim_calendar (
    date DATE PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter VARCHAR(5) NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    day INTEGER NOT NULL,
    day_of_week VARCHAR(15) NOT NULL,
    is_weekend INTEGER NOT NULL,
    is_festive_season INTEGER NOT NULL
);

-- 2. Regions Dimension
CREATE TABLE IF NOT EXISTS dim_regions (
    region_id VARCHAR(20) PRIMARY KEY,
    region VARCHAR(30) UNIQUE NOT NULL,
    primary_hub VARCHAR(50) NOT NULL,
    logistics_cost_tier VARCHAR(20) NOT NULL
);

-- 3. Channels Dimension
CREATE TABLE IF NOT EXISTS dim_channels (
    channel_id VARCHAR(20) PRIMARY KEY,
    channel VARCHAR(50) UNIQUE NOT NULL,
    take_rate_pct NUMERIC(5,4) NOT NULL,
    cost_to_serve_base_pct NUMERIC(5,4) NOT NULL
);

-- 4. Promotions Dimension
CREATE TABLE IF NOT EXISTS dim_promotions (
    promo_id VARCHAR(20) PRIMARY KEY,
    promotion_type VARCHAR(50) UNIQUE NOT NULL,
    default_discount_pct NUMERIC(5,4) NOT NULL,
    vendor_coop_share_pct NUMERIC(5,4) NOT NULL
);

-- 5. Products Dimension
CREATE TABLE IF NOT EXISTS dim_products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    list_price NUMERIC(12,2) NOT NULL,
    unit_cogs NUMERIC(12,2) NOT NULL
);

-- 6. Customers Dimension
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_segment VARCHAR(40) NOT NULL,
    region VARCHAR(30) NOT NULL,
    contract_discount_pct NUMERIC(5,4) NOT NULL,
    created_date DATE NOT NULL
);

-- 7. Normalized Transactions Fact Table
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    date DATE NOT NULL REFERENCES dim_calendar(date),
    customer_id VARCHAR(20) NOT NULL REFERENCES dim_customers(customer_id),
    product_id VARCHAR(20) NOT NULL REFERENCES dim_products(product_id),
    category VARCHAR(50) NOT NULL,
    region VARCHAR(30) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    units INTEGER NOT NULL,
    list_price NUMERIC(12,2) NOT NULL,
    selling_price NUMERIC(12,2) NOT NULL,
    discount NUMERIC(12,2) NOT NULL,
    discount_pct NUMERIC(6,2) NOT NULL,
    revenue NUMERIC(14,2) NOT NULL,
    variable_cost NUMERIC(14,2) NOT NULL,
    gross_profit NUMERIC(14,2) NOT NULL,
    promotion_flag INTEGER NOT NULL,
    promotion_type VARCHAR(50) NOT NULL,
    customer_segment VARCHAR(40) NOT NULL,
    is_outlier INTEGER DEFAULT 0
);
