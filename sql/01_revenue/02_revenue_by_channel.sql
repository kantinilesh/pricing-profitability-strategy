-- Business Question 8: How is net revenue distributed across sales channels?
-- Purpose: Identifies channel scale (Physical Stores vs Direct Web/App vs Marketplace vs Quick-Comm).

SELECT 
    t.channel,
    COUNT(DISTINCT t.transaction_id) AS order_count,
    SUM(t.units) AS units_sold,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.revenue) * 100.0 / SUM(SUM(t.revenue)) OVER (), 2) AS channel_revenue_share_pct,
    ROUND(AVG(t.revenue), 2) AS average_order_value_inr
FROM fact_transactions t
GROUP BY t.channel
ORDER BY total_net_revenue_inr DESC;
