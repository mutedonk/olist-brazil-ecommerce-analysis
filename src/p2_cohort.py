import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

#筛选已送达，取unique_id和购买时间出来
conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT o.order_id,c.customer_unique_id, o.order_purchase_timestamp
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
WHERE o.order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close()

#增加order_month列把购买时间从str转化为时间
df['order_time']=pd.to_datetime(df['order_purchase_timestamp'])
df['order_month']=df['order_time'].dt.to_period('M')

#客户生命周期
lifespan=df.groupby('customer_unique_id')['order_time'].agg(['min','max'])
lifespan['days']=(lifespan['max']-lifespan['min']).dt.days
print(f"Average lifespan of all customers:{lifespan['days'].mean():.1f} days")
print(f"Average lifespan of active customers:{lifespan[lifespan['days']>0]['days'].mean():.1f}days")
print(f"Percentage of active customers:{(lifespan['days']>0).mean():.2%}")

#每行增加每客户最早购买月份(transform不改变行数，没有的填充)
df['first_month']=df.groupby('customer_unique_id')['order_month'].transform('min')

#订单时间距离首次购买月份差（直接相减展示的是月份偏移，把年月拆开相减才是差几个月）
df['month_diff']=(df['order_month'].dt.year - df['first_month'].dt.year) * 12 + (df['order_month'].dt.month - df['first_month'].dt.month)

#同月复购率
first_month_order=df[df['month_diff']==0].groupby('customer_unique_id')['order_id'].nunique()
print(f"Retention rate in the same month:{(first_month_order>1).mean():.2%}")

#按首次购买月份、月数差分组，看每组有多少独立（同月份下多次订单用户被剔除）用户
#首次购买后第n（month_diff）个月回购的客户数
cohort_data = df.groupby(['first_month', 'month_diff'])['customer_unique_id'].nunique().reset_index()
cohort_data.rename(columns={'customer_unique_id': 'active_users'}, inplace=True)

#取月数差为0（基准，该首次购买月的全部独立用户数）的首次购买时间和独立用户书两列
cohort_sizes = cohort_data[cohort_data['month_diff'] == 0][['first_month', 'active_users']].copy()
cohort_sizes.rename(columns={'active_users': 'all_users'}, inplace=True)

#按首月合并基准列（自动填充），回购人数除以基准列人数即为所求
cohort_data = cohort_data.merge(cohort_sizes, on='first_month')
cohort_data['retention_rate'] = cohort_data['active_users'] / cohort_data['all_users']

#数据透视
cohort_matrix=cohort_data.pivot_table(
	index='first_month',
	columns='month_diff',
	values='retention_rate',
	fill_value=0
)

#cohort结论
print(f"Average first month retention rate: {cohort_matrix.iloc[3:,:][1].mean():.2%}")
print(f"Average 3rd month retention rate: {cohort_matrix.iloc[3:,:][3].mean():.2%}")
print(f"Cohort with the highest retention rate: {cohort_matrix.iloc[3:,:][1].max():.2%}")

#画热力图
plt.figure(figsize=(14, 8))
sns.heatmap(
    cohort_matrix.iloc[3:, 1:13],   #去掉值为1的基准列，去掉2016年订单量太少的数据
    annot=True,
    fmt='.2%',
    cmap='YlOrRd',
    linewidths=0.5
)
plt.title('Cohort Retention Rate by First Purchase Month')
plt.xlabel('Months Since First Purchase')
plt.ylabel('Cohort Month')
#plt.savefig(r'outputs\figures\p2_cohort_heatmap_clean.png', dpi=150)
plt.show()

#平均留存率曲线
plt.figure(figsize=(12, 6))
avg_retention = cohort_matrix.iloc[3:, 2:].mean()
plt.plot(
	avg_retention.index, 
	avg_retention.values, 
	marker='o', linewidth=3, markersize=8, 
	color='crimson', label='Average'
)
plt.title('Cohort Retention Curves', fontsize=14)
plt.xlabel('Months Since First Purchase')
plt.ylabel('Retention Rate')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2%}'))
plt.grid(True, alpha=0.3)
#plt.savefig(r'outputs\figures\p2_cohort_avg_retention_curve.png', dpi=150)
plt.show()
