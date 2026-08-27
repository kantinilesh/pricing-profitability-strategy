-- Business Question 7: What is the gross profit and margin % across geographic regions?
-- Purpose: Uncovers regional profitability variances caused by logistics cost tiers (Standard vs High).

SELECT 
    t.region,
    r.primary_hub,
    r.logistics_cost_tier,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.variable_cost), 2) AS total_variable_cost_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct
FROM fact_transactions t
LEFT JOIN dim_regions r ON t.region = r.region
GROUP BY t.region, r.primary_hub, r.logistics_cost_tier
ORDER BY gross_margin_pct DESC;
