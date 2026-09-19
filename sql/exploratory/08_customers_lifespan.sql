WITH ls AS (SELECT CAST(JULIANDAY(MAX(o.order_purchase_timestamp))-JULIANDAY(MIN(o.order_purchase_timestamp)) AS INTEGER) AS lifespan 
FROM orders o 
JOIN customers c ON o.customer_id=c.customer_id
WHERE o.order_status='delivered'
GROUP BY c.customer_unique_id)

SELECT CASE 
	WHEN lifespan=0 THEN '0'
	WHEN lifespan<=30 THEN '0-30'
	WHEN lifespan<=90 THEN '31-90'
	WHEN lifespan<=180 THEN '91-180'
	ELSE '180+'
	END AS range,
	COUNT(*) AS cnt_cus,
	ROUND(100.0*COUNT(*)/SUM(COUNT(*))OVER(),2) AS percentage
FROM ls
GROUP BY range


--Findings:
--97%customers only buy once