-- Business Question 2: What is the monthly gross and net profit contribution over time?
-- Purpose: Evaluates profit trajectory, identifying periods of margin expansion or margin compression.

SELECT 
    cal.year,
    cal.month,
    cal.month_name,
    ROUND(SUM(t.revenue), 2) AS net_revenue_inr,
    ROUND(SUM(t.variable_cost), 2) AS total_variable_cost_inr,
    ROUND(SUM(t.gross_profit), 2) AS monthly_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
    ROUND(
        (SUM(t.gross_profit) - LAG(SUM(t.gross_profit)) OVER (ORDER BY cal.year, cal.month))
        / NULLIF(LAG(SUM(t.gross_profit)) OVER (ORDER BY cal.year, cal.month), 0) * 100, 2
    ) AS mom_profit_growth_pct
FROM fact_transactions t
JOIN dim_calendar cal ON t.date = cal.date
GROUP BY cal.year, cal.month, cal.month_name
ORDER BY cal.year, cal.month;
