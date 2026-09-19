SELECT strftime('%H',order_purchase_timestamp) AS hour, COUNT(*) AS cnt_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY hour
ORDER BY hour



--Findings:
--most orders are purchased between10-22.