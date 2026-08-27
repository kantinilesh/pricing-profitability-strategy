-- Business Question 13: What is the relative revenue, margin, and discount performance across Promotion Types?
-- Purpose: Evaluates campaign effectiveness (Festive Dhamaka vs EOSS Clearance vs Flash Wednesday vs Baseline).

SELECT 
    t.promotion_type,
    t.promotion_flag,
    COUNT(DISTINCT t.transaction_id) AS order_count,
    SUM(t.units) AS units_sold,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.discount * t.units), 2) AS total_discount_given_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
    ROUND(AVG(t.discount_pct), 2) AS avg_discount_pct
FROM fact_transactions t
GROUP BY t.promotion_type, t.promotion_flag
ORDER BY total_net_revenue_inr DESC;
