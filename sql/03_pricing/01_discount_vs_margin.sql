-- Business Question 12: What is the empirical relationship between Discount % tier and Gross Margin %?
-- Purpose: Evaluates discount waterfall leakage across discount tiers (<10%, 10-20%, 20-30%, >30%).

SELECT 
    CASE 
        WHEN t.discount_pct = 0 THEN '0% (Full Price)'
        WHEN t.discount_pct > 0 AND t.discount_pct <= 10 THEN '0.1% - 10.0% (Low Discount)'
        WHEN t.discount_pct > 10 AND t.discount_pct <= 20 THEN '10.1% - 20.0% (Moderate Discount)'
        WHEN t.discount_pct > 20 AND t.discount_pct <= 30 THEN '20.1% - 30.0% (High Discount)'
        ELSE '30.1%+ (Deep Markdown)'
    END AS discount_tier,
    COUNT(DISTINCT t.transaction_id) AS transaction_count,
    SUM(t.units) AS total_units_sold,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND(AVG(t.discount_pct), 2) AS avg_discount_pct,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct
FROM fact_transactions t
GROUP BY 1
ORDER BY avg_discount_pct ASC;
