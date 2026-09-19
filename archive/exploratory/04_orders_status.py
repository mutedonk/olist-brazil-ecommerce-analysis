"""
question_04: What is the distribution of order_status?

SQL vs Python: use value_count() in Python while using GROUP BY and subquery in SQL
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT order_status FROM orders", conn)
conn.close()

status=df['order_status'].value_counts().reset_index()
status.columns=['order_status', 'cnt']
status['percentage']=(100*status['cnt']/ status['cnt'].sum()).round(2)

print(status)