SELECT 'orders' AS table_name, COUNT(*) AS row_cnt FROM orders
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;


-- Findings:
-- The number of rows (99441) in 'orders' table and 'customers' table are the same.
-- The number of rows (112650) in 'order_items' table is not much more than that in 'orders' table, most orders contain only one items.