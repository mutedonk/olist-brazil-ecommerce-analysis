import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

#sql聚合取数
conn = sqlite3.connect(r'data/ecommerce.db')
query=('''
SELECT
	c.customer_state AS state,
	ct.product_category_name_english AS category,
	ROUND(SUM(oi.price),2) AS revenue,
	COUNT(DISTINCT o.order_id) AS order_cnt
FROM orders o
JOIN customers c ON o.customer_id=c.customer_id
JOIN order_items oi ON o.order_id=oi.order_id
JOIN products p ON oi.product_id=p.product_id
JOIN category_translation ct ON p.product_category_name=ct.product_category_name
WHERE o.order_status='delivered'
GROUP BY c.customer_state, ct.product_category_name_english;
''')
df=pd.read_sql_query(query,conn)
conn.close()

#州AOV
df_state=df.groupby('state').agg(
	state_revenue=('revenue','sum'),
	state_cnt=('order_cnt','sum')
).reset_index()
df_state['state_aov']=(df_state['state_revenue']/df_state['state_cnt']).round(2)

#类目AOV
df_cate=df.groupby('category').agg(
	cate_revenue=('revenue','sum'),
	cate_cnt=('order_cnt','sum')
).reset_index()
df_cate['cate_aov']=(df_cate['cate_revenue']/df_cate['cate_cnt']).round(2)
#四象限分类
m_cnt=df_cate['cate_cnt'].median()
m_aov=df_cate['cate_aov'].median()
def classify_cate(row):
	if row['cate_cnt']>=m_cnt and row['cate_aov']>=m_aov:
		return 'Star'
	elif row['cate_cnt']>=m_cnt and row['cate_aov']<m_aov:
		return 'Volume'
	elif row['cate_cnt']<m_cnt and row['cate_aov']>=m_aov:
		return 'Profit'
	else:
		return 'Niche'
df_cate['quadrant']=df_cate.apply(classify_cate,axis=1)
print(df_cate.sort_values('cate_revenue', ascending=False))
#画气泡图
# 四象限颜色
colors = {'Star': '#e74c3c', 'Profit': '#f39c12', 'Volume': '#3498db', 'Niche': '#95a5a6'}

plt.figure(figsize=(12, 8))

for q in colors:
    subset = df_cate[df_cate['quadrant'] == q]
    plt.scatter(
        subset['cate_cnt'], 
        subset['cate_aov'],
        s=subset['cate_revenue'] / 3000,  # 气泡大小=收入
        c=colors[q],
        alpha=0.7,
        label=q,
        edgecolors='black',
        linewidth=0.5
    )
    # 标注Top 5收入类目
    for _, row in subset.head(3).iterrows():
        plt.annotate(
            row['category'][:15],
            (row['cate_cnt'], row['cate_aov']),
            fontsize=8,
            alpha=0.9
        )

# 画分割线
plt.axvline(m_cnt, color='black', linestyle='--', alpha=0.4)
plt.axhline(m_aov, color='black', linestyle='--', alpha=0.4)

plt.xlabel('Order Count (Volume)', fontsize=12)
plt.ylabel('AOV (Value)', fontsize=12)
plt.title('Product Category Strategic Matrix', fontsize=14, fontweight='bold')
plt.legend(title='Quadrant', loc='upper right')
plt.grid(True, alpha=0.3)
#plt.tight_layout()
#plt.savefig(r'outputs\figures\p4_cate_quadrant.png', dpi=150)
plt.show()

#交叉分析
df_state_valid = df_state[df_state['state_cnt'] > 500].sort_values('state_aov', ascending=True)
top5_states = df_state_valid.nlargest(5, 'state_aov')['state'].tolist()
print("高AOV州 Top 5:", top5_states)
df_cross = df[df['state'].isin(top5_states)]
cross_top3 = df_cross.groupby('state').apply(
    lambda x: x.nlargest(3, 'revenue')[['category', 'revenue', 'order_cnt']]
).reset_index(level=1, drop=True)

print("\n高AOV州的Top 3类目：")
print(cross_top3)

bottom5_states = df_state_valid.nsmallest(5, 'state_aov')['state'].tolist()
df_cross_low = df[df['state'].isin(bottom5_states)]
cross_bottom3 = df_cross_low.groupby('state').apply(
    lambda x: x.nlargest(3, 'revenue')[['category', 'revenue', 'order_cnt']]
).reset_index(level=1, drop=True)

print("\n低AOV州的Top 3类目：")
print(cross_bottom3)

# 计算每个州各类目的收入占比
df['pct'] = df.groupby('state')['revenue'].transform(lambda x: x / x.sum() * 100)

# 高AOV州 vs 低AOV州：各类目的平均占比对比
high_states = df_state_valid.nlargest(5, 'state_aov')['state'].tolist()
low_states = df_state_valid.nsmallest(5, 'state_aov')['state'].tolist()

high_profile = df[df['state'].isin(high_states)].groupby('category')['pct'].mean().sort_values(ascending=False)
low_profile = df[df['state'].isin(low_states)].groupby('category')['pct'].mean().sort_values(ascending=False)

# 合并对比
comparison = pd.DataFrame({
    'high_aov_pct': high_profile,
    'low_aov_pct': low_profile
}).fillna(0)

comparison['diff'] = comparison['high_aov_pct'] - comparison['low_aov_pct']
comparison = comparison.sort_values('diff', ascending=False)

print("高AOV州 vs 低AOV州：类目收入占比差异")
print(comparison.head(10).round(2))

# 取差异最大的Top 10类目
top_diff = comparison.head(10)

plt.figure(figsize=(12, 8))
x = range(len(top_diff))
width = 0.35

plt.bar([i - width/2 for i in x], top_diff['high_aov_pct'], width, label='High AOV States', color='#e74c3c', alpha=0.8)
plt.bar([i + width/2 for i in x], top_diff['low_aov_pct'], width, label='Low AOV States', color='#3498db', alpha=0.8)

plt.xticks(x, top_diff.index, rotation=45, ha='right')
plt.ylabel('Avg Revenue Share (%)')
plt.title('Category Preference: High AOV States vs Low AOV States')
plt.legend()
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
#plt.savefig(r'outputs\figures\p4_state_category_comparison.png', dpi=150)
plt.show()