"""
question_03: What is the time span in 'orders' table

SQL vs Python: use COUNT(DISTINCT) in SQL and .nunique() in python, not much different
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query(" SELECT order_purchase_timestamp FROM orders WHERE order_status = 'delivered' ", conn)
conn.close()

ear=df['order_purchase_timestamp'].min()
lat=df['order_purchase_timestamp'].max()
total=df['order_purchase_timestamp'].nunique()

print(f"earlist:{ear}")
print(f"latest:{lat}")
print(f"total:{total}")


