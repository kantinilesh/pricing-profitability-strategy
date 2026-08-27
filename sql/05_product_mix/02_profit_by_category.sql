-- Business Question 5: How does Gross Profit contribution vary across Product Categories?
-- Purpose: Identifies high-margin categories (Apparel, Beauty) vs low-margin categories (Consumer Electronics).

SELECT 
    t.category,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.variable_cost), 2) AS total_variable_cost_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
    ROUND(SUM(t.gross_profit) * 100.0 / SUM(SUM(t.gross_profit)) OVER (), 2) AS profit_share_pct
FROM fact_transactions t
GROUP BY t.category
ORDER BY total_gross_profit_inr DESC;
