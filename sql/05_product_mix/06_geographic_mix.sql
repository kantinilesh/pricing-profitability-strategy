-- Business Question 19: What is the cross-sectional breakdown of Revenue and Margin by Region AND Channel?
-- Purpose: Pinpoints specific region-channel combinations (e.g. North-East E-Commerce) with high cost-to-serve leakage.

SELECT 
    t.region,
    t.channel,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct
FROM fact_transactions t
GROUP BY t.region, t.channel
ORDER BY t.region, gross_margin_pct ASC;
