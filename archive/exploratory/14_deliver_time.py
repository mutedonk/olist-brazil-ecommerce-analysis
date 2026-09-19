"""
question_14: What is the average deliver time in different state?

SQL vs Python: Also when dealing with datetime, we'd better use CAST ... AS INTEGER in sql to remain the same result with python when using dt.days in python. We limit the null time in WHERE clause in sql, and can also use dropna in python to reach the same effect.
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT c.customer_state AS state,o.order_id,order_delivered_customer_date,order_purchase_timestamp
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close()

#处理两列时间去掉空值，把字符串格式转化为日期格式且截断至日
df=df.dropna(subset=['order_delivered_customer_date','order_purchase_timestamp'])
dtime=pd.to_datetime(df['order_delivered_customer_date'])
ptime=pd.to_datetime(df['order_purchase_timestamp'])
df['timediff']=(dtime-ptime).dt.days

#按州分组并聚合order数量和时间平均值
time=df.groupby('state').agg(
	cnt_order=('order_id','count'),
	delivertime=('timediff','mean')
).reset_index()

#去掉订单数小于100的州，按送货时间排序
result=time[time['cnt_order']>100].sort_values('delivertime').reset_index()
print(result.round(2).head(10))
