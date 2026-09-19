--检查项 1：基础摸底（各表规模）
--一共有几张核心表？每张多少行？
SELECT 'orders' AS table_name, COUNT(*) AS rows_count FROM orders
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL 
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL 
SELECT 'products', COUNT(*) FROM products;
--时间范围是什么？数据覆盖多久？
SELECT MAX(order_purchase_timestamp),MIN(order_purchase_timestamp) FROM orders;

-- 检查项 2：缺失值检查
-- 哪些字段有NULL？缺失比例是多少？
-- 缺失有没有规律？（比如早期数据缺失更多？）
SELECT 
	'order_delivered_customer_date' AS column_name,
	COUNT(*)-count(order_delivered_customer_date) AS miss_cnt,
	round(100.0*(COUNT(*)-count(order_delivered_customer_date))/count(*),2) as miss_pct
FROM orders
UNION ALL
SELECT 
	'order_delivered_carrier_date',
	COUNT(*)-count(order_delivered_carrier_date),
	round(100.0*(COUNT(*)-count(order_delivered_carrier_date))/count(*),2)
FROM orders
UNION ALL
SELECT 
	'product_category_name',
	COUNT(*)-count(product_category_name),
	round(100.0*(COUNT(*)-count(product_category_name))/count(*),2)
FROM products
UNION ALL
SELECT 
	'price',
	COUNT(*)-count(price),
	round(100.0*(COUNT(*)-count(price))/count(*),2)
FROM order_items;

--检查项 3：重复值检查
--主键是否唯一？（比如 order_id 在 orders 表里应该唯一吗？）
--customer_unique_id 和 customer_id 的关系是什么？（一个客户可以有多个 customer_id 吗？）
SELECT 'order_id' AS column_name, COUNT(*)-count(DISTINCT order_id) AS duplicate_cnt
FROM orders
UNION ALL
SELECT 'customer_unique_id', COUNT(*)-count(DISTINCT customer_unique_id)
FROM customers
UNION ALL
SELECT 'customer_id', COUNT(*)-count(DISTINCT customer_id)
FROM customers;

--检查项 4：异常值/逻辑错误检查
--日期有没有"倒挂"？（比如发货日期早于下单日期）
SELECT COUNT(*) FROM orders
WHERE order_delivered_carrier_date<order_purchase_timestamp;
--价格有没有异常？（负数、0、极端大值）
SELECT min(price),max(price) FROM order_items;
--订单状态有没有矛盾？（比如状态是 delivered 但送达日期是NULL）
SELECT COUNT(*) FROM orders
WHERE order_status='delivered' 
AND order_delivered_customer_date IS NULL;