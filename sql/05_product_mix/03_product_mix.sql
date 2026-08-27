-- Business Question 18: What is the monthly evolution of Product Category Mix?
-- Purpose: Detects volume shifts from high-margin to low-margin product lines driving company-wide margin compression.

SELECT 
    cal.year,
    cal.quarter,
    t.category,
    SUM(t.units) AS units_sold,
    ROUND(SUM(t.revenue), 2) AS net_revenue_inr,
    ROUND(SUM(t.gross_profit), 2) AS gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct
FROM fact_transactions t
JOIN dim_calendar cal ON t.date = cal.date
GROUP BY cal.year, cal.quarter, t.category
ORDER BY cal.year, cal.quarter, net_revenue_inr DESC;
