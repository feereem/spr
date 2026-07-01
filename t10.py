import pandas as pd,warnings;warnings.filterwarnings('ignore')

c,l = pd.read_csv('output/customers_cleaned.csv'),pd.read_csv('output/Session1_CLTV.csv')

c['k'] = c.churned.astype(str).str.lower().str.strip().isin(['true','yes','y','1'])
cr = round(c.k.mean() * 100,2)

a = l.merge(c).groupby('k')['cltv'].mean().round(2)

pd.DataFrame([{'churn_rate':cr,
               'avg_cltv_churned':a.get(True,0.0),
               'avg_cltv_active':a.get(False,0.0)}])
