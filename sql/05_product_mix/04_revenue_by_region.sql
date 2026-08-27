-- Business Question 6: How is top-line revenue distributed across geographic regions?
-- Purpose: Evaluates regional market penetration and revenue scale.

SELECT 
    t.region,
    r.primary_hub,
    r.logistics_cost_tier,
    COUNT(DISTINCT t.transaction_id) AS order_count,
    SUM(t.units) AS units_sold,
    ROUND(SUM(t.revenue), 2) AS total_net_revenue_inr,
    ROUND(SUM(t.revenue) * 100.0 / SUM(SUM(t.revenue)) OVER (), 2) AS regional_revenue_share_pct
FROM fact_transactions t
LEFT JOIN dim_regions r ON t.region = r.region
GROUP BY t.region, r.primary_hub, r.logistics_cost_tier
ORDER BY total_net_revenue_inr DESC;
