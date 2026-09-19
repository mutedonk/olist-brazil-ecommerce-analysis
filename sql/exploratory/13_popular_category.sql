SELECT 
	ctgr.product_category_name_english AS category,
	COUNT(DISTINCT o.order_id) AS cnt_orders,
	SUM(oi.price) AS total_price
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
JOIN products p ON oi.product_id=p.product_id
JOIN category_translation ctgr ON p.product_category_name=ctgr.product_category_name
WHERE o.order_status='delivered'
GROUP BY category
ORDER BY cnt_orders DESC
LIMIT 10


--Findings:
--The category selling the most number is bed_bath_table, health_beauty  and sports_leisure.
--The category selling the most price is health_beauty , watches_gifts  and bed_bath_table.