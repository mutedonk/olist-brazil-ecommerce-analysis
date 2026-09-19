import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT o.order_purchase_timestamp, c.customer_unique_id, oi.price
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
JOIN order_items oi ON o.order_id=oi.order_id
WHERE o.order_status='delivered'
''')
df=pd.read_sql_query(query,conn)
conn.close()

#找基准日（最大天数+1）
df['order_time']=pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('D')
size=df['order_time'].max()+1

#算R（与基准日直接相减出来的是天数偏移，需转为数字或直接用timestamp格式相减后dt.days）
df_r=df.groupby('customer_unique_id')['order_time'].max().reset_index()
df_r.columns=('customer_unique_id','last_time')
df_r['recency']=(size-df_r['last_time']).apply(lambda x: x.n)
df_r['R_score']=pd.qcut(df_r['recency'],5,labels=[5,4,3,2,1]).astype(int)

#算F（购买次数分布极不均匀，用cut定义切分处理）
df_f=df.groupby('customer_unique_id')['order_time'].count().reset_index()
df_f.columns = ['customer_unique_id', 'frequency']
df_f['F_score']=pd.cut(df_f['frequency'],bins=[0,1,2,3,5,999],labels=[1,2,3,4,5]).astype(int)

#算M（qcut后的列类型是类别不是数值，转换后才能计算）
df_m=df.groupby('customer_unique_id')['price'].sum().reset_index()
df_m['M_score']=pd.qcut(df_m['price'],5,labels=[1,2,3,4,5]).astype(int)

#合并RFM
rfm=df_r[['customer_unique_id','recency','R_score']].merge(df_f).merge(df_m[['customer_unique_id','price','M_score']])

#基于数据特征（F=1客户占97%），按实际业务需求给客户分层（不能直接总分打分）
def segment(row):
	if row['F_score']>=4:			#复购4次+
		return 'VIP Loyal'
	elif row['F_score']>=2:
		if row['R_score']>3:		#复购2-3次，最近来过
			return 'Potential Loyal'
		else:
			return 'At Risk'		#复购过但很久没来
	else:
		if row['R_score']==5:		#最近第一次买
			return'New Customer'
		elif row['R_score']>=3:
			if row['M_score']>=4:		#只买一次，但花得多，最近买的
				return 'One-time High Value'
			elif  row['M_score']>=2:		#只买一次，花得一般，最近买的
				return 'One-time Medium'
			else:
				return 'One-time Low'	##只买一次，花得少，最近买的
		elif row['M_score']>=4:		#只买一次，花得多，但很久没来
			return 'Dormant High Value'
		else:
			return 'Lost'		#只买一次，花得少，很久没来

rfm['segment']=rfm.apply(segment,axis=1)

#统计每分层客户的数量、金额等
segment_stats=rfm.groupby('segment').agg(
	cust_cnt=('customer_unique_id','count'),
	price_avg=('price','mean'),
	price_total=('price','sum')
).reset_index()
segment_stats['pct_customers'] = (segment_stats['cust_cnt'] / segment_stats['cust_cnt'].sum() * 100).round(2)
segment_stats['pct_revenue'] = (segment_stats['price_total'] / segment_stats['price_total'].sum() * 100).round(2)
print(segment_stats.sort_values('cust_cnt', ascending=False))

#客户分层分布
plt.figure(figsize=(14, 8))
order = segment_stats.sort_values('cust_cnt', ascending=True)['segment']
sns.barplot(data=segment_stats, x='cust_cnt', y='segment', order=order, palette='viridis')
plt.title('Customer Segmentation Distribution')
plt.xlabel('Number of Customers')
#plt.savefig(r'outputs\figures\p3_rfm_segments.png', dpi=150)
plt.show()

#各群体收入贡献
plt.figure(figsize=(10, 8))
sns.barplot(data=segment_stats.sort_values('pct_revenue', ascending=False), 
            x='segment', y='pct_revenue', palette='rocket')
plt.title('Revenue Contribution by Segment (%)')
plt.ylabel('% of Total Revenue')
plt.xticks(rotation=30)
#plt.savefig(r'outputs\figures\p3_rfm_revenue.png', dpi=150)
plt.show()
