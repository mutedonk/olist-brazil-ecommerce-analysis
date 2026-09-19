SELECT 
	order_status, 
	COUNT(*) AS cnt, 
	CONCAT(ROUND(100.0* COUNT(*)/ (SELECT COUNT(*) FROM orders), 2), '%' )  AS percentage
FROM orders
GROUP BY order_status
ORDER BY cnt DESC



--Findings:
--over 97% orders were delivered