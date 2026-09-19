"""
question_08: What is the life span of customers?

SQL vs Python: When dealing with the life span, you have to make the time into integer in SQL when using JULIANDAY ,because the float will count customers who buy more than 1 items in a day into the group 0-30, while in python dt.days has already made time into integer.
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query('''
SELECT o.order_purchase_timestamp,c.customer_unique_id FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status='delivered'
''',conn)
conn.close()

#dataframe按顾客分组，增加每个顾客购买的最大、最小时间和时间差
df['time']=pd.to_datetime(df['order_purchase_timestamp'])
span=df.groupby('customer_unique_id')['time'].agg(['min','max']).reset_index()
span['lifespan']=(span['max']-span['min']).dt.days

#把时间差分组
bins=[-1,0,30,90,180,99999]
labels=['0','0-30','30-90','90-180','180+']
span['group']=pd.cut(span['lifespan'], bins=bins, labels=labels)

#按group分组，算每分组顾客行数及占总顾客数百分比
result=span.groupby('group')['customer_unique_id'].size().reset_index()
result.columns=['range','cnt_cus']
result['percentage']=(result['cnt_cus']/len(span)*100).round(2)

print(result)
