"""
question_01: How many rows in tables?

SQL vs Python: use 'UNION ALL' in SQL but loop 3 times in Python
"""


import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')

for table in ['orders' , 'customers' , 'order_items']:
	df=pd.read_sql_query ( f"SELECT * FROM {table}" , conn )
	print(f"{table} : {len(df)} rows")

conn.close()