-- Business Question 9: How do Customer Segments perform in terms of Revenue, Margin, and Discount Rate?
-- Purpose: Identifies high-performing retail customer tiers vs loss-making B2B accounts.

SELECT 
    t.customer_segment,
    COUNT(DISTINCT t.customer_id) AS active_customer_count,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    SUM(t.units) AS total_units_purchased,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.gross_profit), 2) AS total_gross_profit_inr,
    ROUND((SUM(t.gross_profit) / NULLIF(SUM(t.revenue), 0)) * 100, 2) AS gross_margin_pct,
    ROUND(AVG(t.discount_pct), 2) AS avg_discount_rate_pct,
    ROUND(SUM(t.revenue) / COUNT(DISTINCT t.transaction_id), 2) AS average_order_value_inr
FROM fact_transactions t
GROUP BY t.customer_segment
ORDER BY total_net_revenue_inr DESC;
