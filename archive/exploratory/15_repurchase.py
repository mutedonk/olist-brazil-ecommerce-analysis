"""
question_15: What is the average time of customers buy products the 2nd time?

SQL vs Python: use ROW_NUMBER()OVER() in sql to find the 1st and 2nd time a customer bought, while using groupby().nth() in python.
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT c.customer_unique_id,o.order_purchase_timestamp
FROM orders o 
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close()

#转换时间格式，按id、时间排序
df['time']=pd.to_datetime(df['order_purchase_timestamp'])
df=df.sort_values(['customer_unique_id', 'time'])

#找按id分组后第一次和第二次购买时间，并到一张表
first=df.groupby('customer_unique_id').nth(0).reset_index()
second=df.groupby('customer_unique_id').nth(1).reset_index()
merged=first.merge(second, on='customer_unique_id', suffixes=('_1st', '_2st'))

#取时间差，输出均值
merged['diff']=(merged['time_2st']-merged['time_1st'])
print(merged['diff'].mean())