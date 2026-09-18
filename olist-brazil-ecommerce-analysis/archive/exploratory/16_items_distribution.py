"""
question_16: What is the number of items distribute in orders?

SQL vs Python: both use groupby twice
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT o.order_id, oi.price
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
WHERE order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close

item=df.groupby('order_id').agg(
	cnt_item=('price','count'),
	total_price=('price','sum')
).reset_index()
item1=item.groupby('cnt_item').agg(
	cnt_order=('order_id','count'),
	avg_price=('total_price','mean')
).reset_index()

print(item1.round(2))
