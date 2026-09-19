SELECT strftime('%w',order_purchase_timestamp) AS weekday,COUNT(*) AS cnt_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY weekday
ORDER BY weekday


--Findings:
--most orders are purchased on weekdays