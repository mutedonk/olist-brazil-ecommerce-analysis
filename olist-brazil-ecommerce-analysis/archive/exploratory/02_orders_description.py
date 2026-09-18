"""
question_02: What columns in 'orders' table, and what type are they?

SQL vs Python: use PRAGMA in SQL is simple and accurate
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect (r'data/ecommerce.db')
df=pd.read_sql_query ("SELECT * FROM orders", conn)
conn.close

print (df.columns)
print(df.dtypes)

