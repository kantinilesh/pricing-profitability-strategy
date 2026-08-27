-- Business Question 3: How does Gross Margin % vary across Product Categories and Sales Channels?
-- Purpose: Diagnoses structural gross margin variances to uncover low-margin category/channel combinations.

SELECT 
    t.category,
    t.channel,
    ROUND(SUM(t.revenue), 2) AS total_revenue_inr,
    ROUND(SUM(t.variable_cost), 2) AS total_variable_cost_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct
FROM fact_transactions t
GROUP BY t.category, t.channel
ORDER BY gross_margin_pct ASC;
