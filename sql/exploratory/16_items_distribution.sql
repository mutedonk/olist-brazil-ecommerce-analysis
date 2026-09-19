WITH count_items AS (
SELECT o.order_id, COUNT(*) AS cnt_item
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
WHERE order_status='delivered'
GROUP BY o.order_id
)

SELECT 
	cnt_item,
	COUNT(*) AS cnt_order,
	ROUND(AVG(oi.price),2) AS avg_price,
	CONCAT(ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM orders WHERE order_status='delivered'),2),'%') AS percentage
FROM count_items ci
JOIN order_items oi ON ci.order_id=oi.order_id
GROUP BY cnt_item


--Findings:
--90% orders just buy 1 item and the average price is 129.7, there's also orders with 21 items but only 0.02%.