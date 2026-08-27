# Data Dictionary: Pricing & Profitability Strategy Platform

This document describes the schema, field definitions, data types, and business logic for the primary analytical dataset and supporting dimension tables.

---

## 1. Primary Analytical Fact Table (`analytical_dataset.csv`)

| Column Name | Data Type | Description / Definition | Business Calculation / Source |
|---|---|---|---|
| `transaction_id` | STRING | Unique primary key for each retail order line. | `TXN_000001` format |
| `date` | DATE | Transaction date (`YYYY-MM-DD`). | Foreign Key to `dim_calendar` |
| `year` | INTEGER | Calendar year (2024 or 2025). | Extracted from `date` |
| `quarter` | STRING | Calendar quarter (`Q1`, `Q2`, `Q3`, `Q4`). | Extracted from `date` |
| `month` | INTEGER | Month number (1 to 12). | Extracted from `date` |
| `month_name` | STRING | Month name (`January` to `December`). | Extracted from `date` |
| `day_of_week` | STRING | Day of week (`Monday` to `Sunday`). | Extracted from `date` |
| `is_weekend` | INTEGER | Indicator if transaction occurred on weekend (`1`=Yes, `0`=No). | Binary flag |
| `is_festive_season` | INTEGER | Indicator if transaction occurred in Diwali/Navratri season (Oct-Nov). | Binary flag |
| `customer_id` | STRING | Unique identifier for buyer account. | Foreign Key to `dim_customers` |
| `customer_name` | STRING | Name of client account or retail customer. | From `dim_customers` |
| `customer_segment` | STRING | Customer tier (`B2B Enterprise`, `B2B SMB`, `Retail Platinum`, `Retail Gold`, `Retail Silver`, `Retail Standard`). | Segment classification |
| `contract_discount_pct` | FLOAT | Contractual discount rate agreed for account (0.0 to 0.22). | From `dim_customers` |
| `product_id` | STRING | Unique SKU identifier. | Foreign Key to `dim_products` |
| `product_name` | STRING | Product descriptive name. | From `dim_products` |
| `category` | STRING | Main product category (`Consumer Electronics`, `Apparel & Fashion`, `Home & Kitchen`, `FMCG & Personal Care`, `Footwear`, `Beauty & Cosmetics`). | Standardized category |
| `subcategory` | STRING | Subcategory level 2 classification. | From `dim_products` |
| `region` | STRING | Geographic sales region (`North`, `South`, `West`, `East`, `Central`, `North-East`). | From `dim_customers` / `dim_regions` |
| `primary_hub` | STRING | Primary regional distribution logistics hub (e.g. `Delhi NCR`, `Bengaluru`, `Mumbai`). | From `dim_regions` |
| `logistics_cost_tier` | STRING | Logistics freight cost classification (`Standard`, `Medium`, `High`). | From `dim_regions` |
| `channel` | STRING | Sales distribution channel (`Physical Retail Store`, `E-Commerce Direct`, `E-Commerce Marketplace`, `Quick-Commerce`). | Sales channel |
| `take_rate_pct` | FLOAT | Channel partner take rate / commission fee (e.g., 0.10 for Marketplace). | From `dim_channels` |
| `cost_to_serve_base_pct` | FLOAT | Baseline fulfillment cost-to-serve as % of revenue. | From `dim_channels` |
| `units` | INTEGER | Physical quantity of items purchased. | Order quantity |
| `list_price` | FLOAT | Sticker MSRP list price per unit in INR. | Baseline list price |
| `selling_price` | FLOAT | Realized net selling price per unit in INR after all discounts. | `list_price - discount` |
| `discount` | FLOAT | Total discount per unit in INR. | `list_price - selling_price` |
| `discount_pct` | FLOAT | Total discount percentage realized. | `(discount / list_price) * 100` |
| `revenue` | FLOAT | Total net revenue in INR. | `units * selling_price` |
| `variable_cost` | FLOAT | Total variable cost (COGS + Channel Logistics) in INR. | `(units * unit_cogs) + fulfillment` |
| `gross_profit` | FLOAT | Gross profit contribution in INR. | `revenue - variable_cost` |
| `gross_margin_pct` | FLOAT | Gross profit contribution percentage. | `(gross_profit / revenue) * 100` |
| `promotion_flag` | INTEGER | Indicator if transaction was promotional (`1`=Yes, `0`=No). | Binary flag |
| `promotion_type` | STRING | Promotion campaign type (`Festive Dhamaka`, `Navratri Special`, `EOSS Clearance`, `Flash Wednesday`, `B2B Volume Incentive`, `Baseline / None`). | Promo type |
| `vendor_coop_share_pct` | FLOAT | Manufacturer co-op funding share of promo discount. | From `dim_promotions` |
| `is_outlier` | INTEGER | Flag indicating high-unit outlier transaction (`1`=units>500, `0`=normal). | Quality indicator |

---

## 2. Supporting Dimension Tables

### 2.1 `dim_customers.csv`
- `customer_id` (PK): Unique customer identifier.
- `customer_name`: Name of customer account.
- `customer_segment`: Segment tier.
- `region`: Primary operating region.
- `contract_discount_pct`: Agreed contract discount percentage.
- `created_date`: Account creation date.

### 2.2 `dim_products.csv`
- `product_id` (PK): Unique product SKU identifier.
- `product_name`: Descriptive product name.
- `category`: Primary product category.
- `subcategory`: Secondary product classification.
- `list_price`: Base MSRP list price.
- `unit_cogs`: Base manufacturing/procurement cost per unit.

### 2.3 `dim_regions.csv`
- `region_id` (PK): Region code.
- `region`: Region name.
- `primary_hub`: Main logistics hub city.
- `logistics_cost_tier`: Freight cost tier.

### 2.4 `dim_channels.csv`
- `channel_id` (PK): Channel identifier.
- `channel`: Channel name.
- `take_rate_pct`: Channel commission / fee percentage.
- `cost_to_serve_base_pct`: Baseline fulfillment cost percentage.

### 2.5 `dim_promotions.csv`
- `promo_id` (PK): Promotion identifier.
- `promotion_type`: Campaign name.
- `default_discount_pct`: Standard campaign discount.
- `vendor_coop_share_pct`: Vendor co-op funding share.

### 2.6 `dim_calendar.csv`
- `date` (PK): Calendar date (`YYYY-MM-DD`).
- `year`, `quarter`, `month`, `month_name`, `day`, `day_of_week`, `is_weekend`, `is_festive_season`.
