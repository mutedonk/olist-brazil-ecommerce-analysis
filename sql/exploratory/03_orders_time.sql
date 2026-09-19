SELECT 
	MAX(order_purchase_timestamp) AS latest, 
	MIN(order_purchase_timestamp) AS earlist, 
	COUNT( DISTINCT order_purchase_timestamp) AS total
FROM orders
WHERE order_status = 'delivered';



--Findings:
--The orders spread in 2 years