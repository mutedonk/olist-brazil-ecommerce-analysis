"""
question_09: How the number of orders change by month?

SQL vs Python: both use one groupby can have the result
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT order_purchase_timestamp FROM orders WHERE order_status='delivered'",conn)
conn.close()

df['time']=pd.to_datetime(df['order_purchase_timestamp'])
monthly=df.groupby(df['time'].dt.to_period('M')).size().reset_index()
monthly.columns=['month','cnt_orders']

print(monthly)