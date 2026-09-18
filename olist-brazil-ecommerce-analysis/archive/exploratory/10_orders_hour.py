"""
question_10: How the number of orders change by hour?

SQL vs Python: both use one groupby can have the result
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT order_purchase_timestamp FROM orders WHERE order_status='delivered'",conn)
conn.close()

df['time']=pd.to_datetime(df['order_purchase_timestamp'])
hours=df.groupby(df['time'].dt.hour).size().reset_index()
hours.columns=['hour','cnt_orders']

print(hours)

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))
plt.plot(hours['hour'], hours['cnt_orders'], marker='o')
plt.title('Orders by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Count')
plt.xticks(range(24))
plt.grid(True, alpha=0.3)
plt.savefig('orders_by_hour.png')
plt.show()