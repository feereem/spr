import pandas as pd,matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
c = pd.read_csv('cclean.csv')

with PdfPages('Graph5.pdf') as pdf:
    ax = pd.cut(c['age'],[17,24,34,44,200],labels=['18-24','25-34','35-44','45+']).value_counts().sort_index().plot.bar(title='gender',ylabel='total',rot=0,color='#1338BE')
    ax.set_axisbelow(True)
    ax.grid(axis='y',ls='--')
    pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()

    g = c[c['gender'].isin(['M','F'])]['gender'].value_counts(normalize=True).mul(100).map('{:,.2f}'.format).reset_index()
    t = c[c['membership_status'].isin(['Basic','Silver','Gold'])].groupby('membership_status')['total_spending'].mean().map('{:,.0f}'.format).reset_index()

    data = [('ti1',g,['gender','total']),('ti2',t,['tier','total'])]
    for ti,df,col in data:
        fig,ax = plt.subplots(figsize=(6,2));ax.axis('off')
        ax.set_title(ti,weight='bold',fontsize=14,pad=20)
        ax.table(cellText=df.values,colLabels=col,loc='center',cellLoc='center').scale(1,2)
        pdf.savefig(plt.gcf(),bbox_inches='tight');plt.close()
