"""
question_07: How many customers in different state and how many items they bought?

SQL vs Python: no much different in two methods, maybe easier when counting 'order_per_cus'
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query('''
SELECT c.customer_state, c.customer_unique_id, o.order_id FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
WHERE o.order_status='delivered'
''',conn)
conn.close()

result=df.groupby('customer_state').agg(
	cnt_cus=('customer_unique_id','nunique'),
	cnt_orders=('order_id','count')
).reset_index()
result['order_per_cus'] = (result['cnt_orders'] / result['cnt_cus']).round(2)
result = result.sort_values('cnt_cus', ascending=False).head(10)

print(result)
