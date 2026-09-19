SELECT 
	c.customer_state, 
	COUNT(DISTINCT o.order_id) AS cnt_o,
	ROUND(SUM(oi.price),2) AS total_price,
	ROUND(SUM(oi.price)/COUNT(DISTINCT o.order_id),2) AS per_price
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status= 'delivered'
GROUP BY c.customer_state
HAVING cnt_o>100
ORDER BY per_price DESC


--Findings:
--When we join the 3 tables, order_id will have duplicate values (because of the order_items table)
--The highest AOV is in state PB, but the number of orders is not that much. The state with most orders likeRJ, MG, SP has low AOV.
