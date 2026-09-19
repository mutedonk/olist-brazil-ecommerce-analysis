SELECT 
	c.customer_state AS state,
	COUNT(o.order_id) AS cnt_order,
	ROUND(AVG(CAST(JULIANDAY(order_delivered_customer_date)-JULIANDAY(order_purchase_timestamp) AS INTEGER)) ,2) AS delivertime
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
	AND o.order_delivered_customer_date IS NOT NULL
	AND o.order_purchase_timestamp IS NOT NULL
GROUP BY c.customer_state
HAVING COUNT(o.order_id)>100
ORDER BY delivertime
LIMIT 10


--Findings:
--The state selling the most number has the least delivering time,always less than 15 days.
--In this question we have to limit the time column(o.order_delivered_customer_date,o.order_purchase_timestamp) is not null, otherwise the result will be inaccurate.