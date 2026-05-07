import pandas as pd,matplotlib.pyplot as plt,matplotlib.ticker as mt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import StrMethodFormatter as smf

p,s = pd.read_csv('products.csv'),pd.read_csv('sclean.csv')
for col in ['price','cost']:
    p[col] = pd.to_numeric(p[col].astype(str).str.replace(r'^0-9.\-','',regex=True),errors='coerce').abs()
p['category'] = p['category'].replace({'Pastry':'Pastries'})

m = s.assign(
    revenue = (s['quantity'] * s['price']) - pd.to_numeric(s['discount_amount']).fillna(0)
).merge(p[['product_id','product_name','category','cost']],on='product_id',how='left')

t3 = m.groupby('product_name')[['quantity','revenue']].sum().nlargest(3,'quantity').reset_index()
t3['revenue'] = t3['revenue'].map('${:,.2f}'.format)
cr = m[m.category.isin(['Bread','Tarte','Pastries'])].groupby('category')['revenue'].sum()

with PdfPages('abc.pdf') as pdf:
    fig,ax = plt.subplots();
    cr.plot.bar(color=['red','green','blue'],rot=0,ylabel='Total Revenue ($)')
    ax.set_title('CAT',weight='bold',fontsize=14)
    ax.grid(axis='y',ls='--')
    ax.yaxis.set_major_formatter(smf('${x:,.0f}'))
    ax.set_axisbelow(True)
    pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()
    fig,t = plt.subplots(figsize=(6,2));t.axis('off')
    t.table(cellText=t3.values,colLabels=['gg','ggh','gfg'],loc='center',cellLoc='center').scale(1,2)
    pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()
