import pandas as pd
import sqlite3
import os

folder = r'data'
db_path = os.path.join(folder, 'ecommerce.db')
conn = sqlite3.connect(db_path)

files = {
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'category_translation': 'product_category_name_translation.csv',
    'orders': 'olist_orders_dataset.csv',
    'customers': 'olist_customers_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv'
}

for table, filename in files.items():
    try:
        pd.read_csv(os.path.join(folder, filename), encoding='utf-8-sig').to_sql(
            table, conn, index=False, if_exists='replace'
        )
        print(f"✅ {table} Import Successed")
    except Exception as e:
        print(f"⚠️ {table} Import Failed: {e}")

conn.close()