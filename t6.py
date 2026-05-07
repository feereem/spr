import pandas as pd,warnings;warnings.filterwarnings('ignore')
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv('sclean.csv')
s['date'] = pd.to_datetime(s['date']).dt.normalize()

daily = s.assign(rev=(s.quantity * s.price) - s.discount_amount.fillna(0)).groupby('date')['rev'].sum().sort_index()

split = int(len(daily) * .8)
f = lambda x,n: ARIMA(x,order=(1,1,1)).fit().forecast(steps=n)
print(f'MAE: {(daily.iloc[split:] - f(daily.iloc[:split],len(daily)-split)).abs().mean():.2f}')

pd.DataFrame({'Date':pd.date_range(daily.index[-1] + pd.Timedelta(days=1),periods=30).strftime('%Y-%m-%d'),'Predected_Sales':f(daily,30).values.round(2)}).to_csv('t6.csv',index=False)
