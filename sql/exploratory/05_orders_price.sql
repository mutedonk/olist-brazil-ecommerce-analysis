WITH sumprice AS( SELECT SUM(oi.price) AS sp FROM orders o 
JOIN order_items oi ON o.order_id=oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY o.order_id
)

SELECT 
	ROUND(MIN(sp) , 2) AS min_price,
	ROUND(MAX(sp) , 2) AS max_price,
	ROUND(AVG(sp) , 2) AS avg_price
FROM sumprice



--Findings:
--Average order price is 137