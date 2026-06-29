import pandas as pd,numpy as np,warnings;warnings.filterwarnings('ignore')
s,p = pd.read_csv('output/sales_transactions_cleaned.csv'),pd.read_csv('file/products.csv')

s['rev'] = (s.quantity * s.price) - s.discount_amount.fillna(0)
p['c'] = pd.to_numeric(p.cost.astype(str).str.replace(r'[0-9./-]','',regex=1),errors='coerce')

f = s.groupby('product_id',as_index=0).agg(
    total_quantity_sold = ('quantity','sum'),
    total_revenue = ('rev','sum')
).merge(p[['product_id','c']])
f['profit_matgin'] = (1 - f.total_quantity_sold * f.c / f.total_revenue).round(4)
f.drop(columns='c').sort_values('total_revenue',ascending=0).round(2).to_csv('output/Session5_Product_Performance_short_short.csv',index=0)

sale_month = s.assign(
    month=pd.to_datetime(s['date']).dt.strftime('%Y-%m')
)

monthly_sale = (
    sale_month
    .groupby(['product_id','month'])
    .agg(
        quantity = ('quantity','sum'),
        price = ('price','mean')
    )
)

monthly_sale['quantity_change'] = (
    monthly_sale
    .groupby('product_id')['quantity']
    .pct_change()
)

monthly_sale['price_change'] = (
    monthly_sale
    .groupby('product_id')['price']
    .pct_change()
)

monthly_sale['elasticity'] = (
    monthly_sale['quantity_change'] / monthly_sale['price_change']
)

monthly_sale['elasticity'] = (
    monthly_sale['elasticity'].replace([np.inf, -np.inf],np.nan)
)

d = (
    monthly_sale.groupby('product_id')['elasticity'].mean().round(4).reset_index()
)

d['suggested_price_change'] = d['elasticity'].apply(
    lambda x:
        '-5%' if x < -1
        else '+5%' if -1 <= x < 0
        else '0%'
)

d = d.rename(
    columns={
        'elasticity' : 'price_elasticity_of_demand'
    }
)
d.to_csv('output/Session5_Price_Analysis.csv')
