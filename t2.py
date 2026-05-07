import pandas as pd,numpy as np

s,c = pd.read_csv('sales_transactions.csv'),pd.read_csv('customers.csv')

c['age'] = c['age'].fillna(c['age'].median())
c['phone_number'] = c['phone_number'].fillna('0').astype(str).str.replace(r'[^0-9+]','',regex=True).replace(['','00'],'0')
s['promotion_id'] = s['promotion_id'].fillna('0')

def dt(x):
    x = pd.to_datetime(x.fillna('2024-01-014'),errors='coerce',format='mixed')
    x =x.where((x.dt.year >=2000) & (x.dt.year <=2025))
    return x + pd.to_timedelta(np.random.randint((9*3600),(17*3600+1),len(x)),unit='s')

c['last_purchase_date'] = dt(c['last_purchase_date'])
c['join_date'] = dt(c['join_date'])
s['date'] = dt(s['date'])

s.to_csv('sclean.csv',index=False)
c.to_csv('cclean.csv',index=False)
