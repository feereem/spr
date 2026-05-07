import pandas as pd,warnings;warnings.filterwarnings('ignore')

s = pd.read_csv('sclean.csv')
m = pd.to_datetime(s.date).dt.to_period('M').nunique()

c = s.assign(rev = (s.quantity * s.price) - s.discount_amount.fillna(0)).groupby('customer_id',as_index=False)['rev'].sum().assign(
    customer_id = lambda x:x.customer_id.astype(int),
    cltv=lambda x: (x.rev * 36 / m).round(2))[['customer_id','cltv']]

c.to_csv('CLTV.csv',index=False)
