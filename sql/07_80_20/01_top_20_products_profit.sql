-- Business Question 10: Which products constitute the Top 20% of SKUs by total gross profit contribution?
-- Purpose: Identifies core value driver SKUs for inventory prioritization and margin protection.

WITH product_profit_ranks AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.list_price,
        SUM(t.units) AS units_sold,
        ROUND(SUM(t.revenue), 2) AS total_revenue_inr,
        ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
        ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
        NTILE(5) OVER (ORDER BY SUM(t.gross_profit) DESC) AS profit_quintile
    FROM fact_transactions t
    JOIN dim_products p ON t.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.list_price
)
SELECT 
    product_id,
    product_name,
    category,
    list_price,
    units_sold,
    total_revenue_inr,
    total_gross_profit_inr,
    gross_margin_pct
FROM product_profit_ranks
WHERE profit_quintile = 1  -- Top 20% Quintile
ORDER BY total_gross_profit_inr DESC;
