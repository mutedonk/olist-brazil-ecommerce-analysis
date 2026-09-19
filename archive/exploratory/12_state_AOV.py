"""
question_12: What is the AOV in different state?

SQL vs Python: nearly the same
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect(r'data/ecommerce.db')
query='''
SELECT o.order_id, oi.price, c.customer_state
FROM orders o
JOIN order_items oi ON o.order_id=oi.order_id
JOIN customers c ON o.customer_id=c.customer_id
WHERE order_status= 'delivered'
'''
df=pd.read_sql_query(query,conn)
conn.close()

aov=df.groupby(df['customer_state']).agg(
	cnt_o=('order_id','nunique'),
	total_price=('price','sum')
).reset_index()
aov['per_price']=(aov['total_price']/aov['cnt_o']).round(2)

result=aov[aov['cnt_o']>100].sort_values('per_price',ascending=False)
print(result)

result.plot(kind='bar', x='customer_state', y='per_price', figsize=(10, 6))
plt.show()
