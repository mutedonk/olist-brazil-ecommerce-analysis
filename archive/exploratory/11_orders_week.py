"""
question_11: How the number of orders change by day of week?

SQL vs Python: use strftime('%w') in sql and dt.dayofweek in python can give the result, but in sql 0=Sunday,1=Monday,etc.  while in python 0=Monday, 1=Tuesday,etc. or we also can use dt.day_name() in python but it is not the order we want (we can reorder it). In this case i use dt.dayoftime and map in python can have the best result.
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT order_purchase_timestamp FROM orders WHERE order_status='delivered'",conn)
conn.close()

df['time']=pd.to_datetime(df['order_purchase_timestamp'])
weekday=df.groupby(df['time'].dt.dayofweek).size().reset_index()
weekday.columns=['weekday','cnt_orders']

wmap={0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
weekday['weekday']=weekday['weekday'].map(wmap)
print(weekday)