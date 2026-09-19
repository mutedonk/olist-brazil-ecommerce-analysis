SELECT
	c.customer_state AS state,
	ct.product_category_name_english AS category,
	ROUND(SUM(oi.price),2) AS Revenue,
	COUNT(DISTINCT o.order_id) AS Order_Count,
	ROUND(SUM(oi.price)/COUNT(DISTINCT o.order_id),2) AS AOV
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
JOIN order_items oi ON o.order_id=oi.order_id
JOIN products p ON oi.product_id=p.product_id
JOIN category_translation ct ON p.product_category_name=ct.product_category_name
WHERE o.order_status='delivered'
GROUP BY c.customer_state, ct.product_category_name_english;




