"""
question_05: What is the price every order?

SQL vs Python: use 3 aggregate function in SQL while using just a describe() in python
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT o.order_id, oi.price FROM order_items oi JOIN orders o ON o.order_id=oi.order_id WHERE o.order_status='delivered'", conn)
conn.close

sumprice=df.groupby('order_id')['price'].sum()
print(sumprice.describe())