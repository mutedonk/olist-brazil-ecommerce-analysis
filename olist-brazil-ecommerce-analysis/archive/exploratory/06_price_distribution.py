"""
question_06: What is the price distribute in different range

SQL vs Python: use a long CASE WHEN in sql while using pd.cut() then groupby in python, a little easier in python
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
df=pd.read_sql_query("SELECT price FROM order_items", conn)
conn.close()

bins=[0,50,100,150,200,250,300,14000]
labels=['0-50','50-100','100-150','150-200','200-250','250-300','300+']
df['range']= pd.cut(df['price'], bins=bins, labels=labels, right=False)
group_by=df.groupby('range').agg(
	cnt_p=('price','count'),
	sum_p=('price','sum')
)
print(group_by)
