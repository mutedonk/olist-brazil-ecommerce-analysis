"""
question_17: What is the price distribute in orders in percentile?

"""

import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query = """
SELECT o.order_id, oi.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
"""
df = pd.read_sql_query(query, conn)
conn.close()

df=df.groupby('order_id')['price'].sum()

for p in [10, 25, 50, 75, 90, 95, 99]:
    print(f"P{p}: {df.quantile(p/100):.2f}")