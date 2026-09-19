import pandas as pd
import sqlite3

conn = sqlite3.connect(r'data/ecommerce.db')
query1=("SELECT * FROM orders")
query2=("SELECT * FROM customers")
query3=("SELECT * FROM order_items")
query4=("SELECT * FROM products")
orders=pd.read_sql_query(query1,conn)
customers=pd.read_sql_query(query2,conn)
order_items=pd.read_sql_query(query3,conn)
products=pd.read_sql_query(query4,conn)
conn.close()

# ========== 1. 基础检查 ==========
print(f"{'='*50}")
print("1.Data Overview")
def check_data_quality(df,table_name):
	print(f"\ntable name:{table_name}")
	#1.基础信息 basic information
	print(f"Row Count:{len(df)} | Column Count:{len(df.columns)}")
	#2.空值检查 null check
	null_col=df.isnull().sum()[df.isnull().sum()>0]
	if len(null_col)>0 :
		print(f"missing values columns ({len(null_col)} columns)")
		for col,cnt in null_col.items():
			pct= 100.0*cnt/len(df)
			print(f"{col}:{cnt} missing values ({pct:.2f}%)")
	else: print("no missing values")

tables = {
    'orders': orders,
    'customers': customers,
    'order_items': order_items,
    'products': products,
}
for name, df in tables.items():
	check_data_quality(df,name)
print(f"{'='*50}")

# ========== 2. 重复值检查（主键） ==========
print("2.Duplicates Check\n")
key_checks={
	'orders':'order_id',
	'customers':'customer_unique_id',
	'products': 'product_id',
}
for table, key_col in key_checks.items():
	df = tables[table]
	dup_rate = df[key_col].duplicated().sum() / len(df)
	if dup_rate > 0:
		print(f" {table}.{key_col} Duplication Rate: {dup_rate:.2%}")
	else: 
		print(f"  {table}.{key_col}: No duplicates")
print(f"{'='*50}")

# ========== 3. 外键检查 ==========
print("3.Referential Integrity\n")
def check_relationships():
	orphan_items=set(order_items['order_id']) - set(orders['order_id'])
	print(f"order_items.order_id not in orders: {len(orphan_items)}")
	orphan_cus=set(orders['customer_id']) - set(customers['customer_id'])
	print(f"orders.customer_id not in customers: {len(orphan_cus)}")
	orphan_products = set(order_items['product_id']) - set(products['product_id'])
	print(f"order_items.product_id not in products: {len(orphan_products)}")
	print(f"order_status values: {orders['order_status'].unique()}")

check_relationships()
print(f"{'='*50}")

# ========== 4. 异常值检查 ==========
print("4.Outlier Check\n")
def check_outlier():
	#1.日期倒挂 Negative delivery time（发货时间早于下单时间）
	orders_temp=orders.copy()
	orders_temp['delivered']=pd.to_datetime(orders_temp['order_delivered_carrier_date'])
	orders_temp['purchase']=pd.to_datetime(orders_temp['order_purchase_timestamp'])
	time=orders_temp[orders_temp['delivered']<orders_temp['purchase']]
	print(f"  Negative delivery time : {len(time)}")
	#2.金额为负或0 Non-positive price
	price=order_items[order_items['price']<=0]
	print(f"  Non-positive price: {len(price)}")
	#3.极端值 Extreme price
	q99=order_items['price'].quantile(0.99)
	extreme=order_items[order_items['price']>q99*10]
	print(f"  Extreme high price (>10x P99): {len(extreme)}")

check_outlier()
print(f"{'='*50}")