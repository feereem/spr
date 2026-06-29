import pandas as pd,warnings;warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans;
from sklearn.preprocessing import StandardScaler

s = pd.read_csv('output/sales_transactions_cleaned.csv')

f = s.assign(rev=(s.quantity * s.price) - s.discount_amount.fillna(0)).groupby('customer_id').agg(
    tx = ('transaction_id','nunique'),
    rev = ('rev','mean')
).reset_index()

f['c'] = KMeans(3,n_init=10,random_state=42).fit_predict(StandardScaler().fit_transform(f[['tx','rev']])) + 1

tp = s.merge(f[['customer_id','c']]).groupby(['c','product_id']).quantity.sum().sort_values(ascending=0).reset_index().groupby('c').product_id.agg(list)

pu = s.groupby('customer_id').product_id.agg(set)

row=[]

for u,c in zip(f.customer_id,f.c):
    recomment = [
        p for p in tp[c]
        if p not in pu[u]
    ]
    recomment = recomment[:3]
    recomment += [None] * (3 - len(recomment))
    
    row.append(
        [u,c] + recomment
    )

pd.DataFrame(
    row,
    columns=[
        'customer_id',
        'cluster_label',
        'recommended_product_1',
        'recommended_product_2',
        'recommended_product_3'
    ]
).to_csv('output/Session5_Segmentation_and_Recommendations.csv',index=False)
