SELECT CASE
	WHEN price<50 THEN '0-50'
	WHEN price<100 THEN '50-100'
	WHEN price<150 THEN '100-150'
	WHEN price<200 THEN '150-200'
	WHEN price<250 THEN '200-250'
	WHEN price<300 THEN '250-300'
	ELSE '300+'
	END AS range,
	COUNT(*) AS cnt,
	ROUND(SUM(price),2) AS total	
FROM order_items
GROUP BY range


--Findings:
--most item price is between 0 and 100, and the highest total price is in the range of over 300.