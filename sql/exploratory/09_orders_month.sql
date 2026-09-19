SELECT strftime('%Y-%m',order_purchase_timestamp) AS month, COUNT(*) AS cnt_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY month
ORDER BY month



--Findings:
--The number of orders keep growing between 2017-01 and 2017-11, with the large quantity in 2017-11, and remain stable afterward.