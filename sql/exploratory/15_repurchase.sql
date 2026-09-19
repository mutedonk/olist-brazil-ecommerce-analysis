WITH ranked AS (
SELECT 
	c.customer_unique_id,
	o.order_purchase_timestamp,
	ROW_NUMBER()OVER(PARTITION BY c.customer_unique_id ORDER BY o.order_purchase_timestamp) AS rn
FROM orders o 
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
)

SELECT ROUND(AVG(JULIANDAY(r2.order_purchase_timestamp)-JULIANDAY(r1.order_purchase_timestamp)),2) AS time
FROM ranked r1
JOIN ranked r2 ON r1.customer_unique_id=r2.customer_unique_id
WHERE r1.rn=1 AND r2.rn=2



--Findings:
--The average time of customers buy pruducts 2nd time is 81.21 days.