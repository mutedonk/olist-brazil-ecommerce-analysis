"""
question_13: What is the popular category?

SQL vs Python: both groupby and aggregate
"""

import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT o.order_id, ctgr.product_category_name_english AS category, oi.price
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
JOIN products p ON oi.product_id=p.product_id
JOIN category_translation ctgr ON p.product_category_name=ctgr.product_category_name
WHERE o.order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close()

result=df.groupby('category').agg(
	cnt_order=('order_id','nunique'),
	total_price=('price','sum')
).sort_values('cnt_order', ascending=False).head(10).reset_index()

print(result)