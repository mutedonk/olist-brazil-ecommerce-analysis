SELECT 
	c.customer_state,
	COUNT(DISTINCT c.customer_unique_id) AS cnt_cus,
	COUNT(o.order_id) AS cnt_orders,
	ROUND(COUNT(o.order_id) * 1.0 / COUNT(DISTINCT c.customer_unique_id), 2) AS order_per_cus
FROM orders o 
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
GROUP BY customer_state
ORDER BY cnt_cus DESC
LIMIT 10



--Findings:
--The customers in SP is the most and most customers buy 1 item