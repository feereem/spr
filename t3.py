import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import StrMethodFormatter as smf
df = pd.read_csv('s-Clean.csv')

df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
df['revenue'] = (df['quantity'] * df['price']) - pd.to_numeric(df['discount_amount']).fillna(0)

stat = df.groupby('date').agg(
    rev = ('revenue','sum'),
    tx = ('transaction_id','nunique')
).assign(aov = lambda x:x['rev'] / x['tx']).sort_index().reset_index()

t3 = stat.nlargest(3,'rev')[['date','rev']].assign(
    rev = lambda x:x['rev'].apply(lambda v:f"${v:,.2f}")
).reset_index(drop=True)

data = [('rev','red','g1'),('tx','red','g1'),('aov','red','g1')]

with PdfPages('filmtests3.pdf') as pdf:
    for col,cl,ti in data:
        fig,ax = plt.subplots(figsize=(10,5))
        ax.set_title(ti,weight='bold',fontsize=14)
        ax.plot(stat['date'],stat[col],marker='o',color=cl)
        ax.grid(axis='y',ls='-')
        if col in ['rev','aov']:
            ax.yaxis.set_major_formatter(smf('${x:,.0f}'))
        pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()
    fig,ax = plt.subplots(figsize=(6,2));ax.axis('off')
    ax.set_title('TOP 3',weight='bold',fontsize=14)
    ax.table(cellText=t3.values,colLabels=['Month','Total Revenue'],loc='center',cellLoc='center',colColours=['skyblue','skyblue']).scale(1,2)
    pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()
