import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL']
data = yf.download(tickers = companies,
            period = "6y",
            interval = "1d",
            prepost = False,
            repair = True) 

df = pd.DataFrame(columns=['ds', 'y'])

df['ds'] = pd.to_datetime(data.index)
df['y'] = data.Open.AAPL.values

m = Prophet()
m.add_seasonality(name='quarterly', period=91.5, fourier_order=8)
m.fit(df)
future = m.make_future_dataframe(periods=200)

forecast = m.predict(future)
# fig = m.plot_components(forecast)

plt.figure(figsize=(15, 7))
plt.plot(forecast['ds'], forecast['yhat_upper'], color='lightblue')
plt.plot(forecast['ds'], forecast['yhat_lower'], color='lightblue')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=1)
plt.plot(forecast['ds'], forecast['yhat'], color='blue')
plt.plot(data.Open.AAPL,color='green')
plt.xlabel('Time (years)')
plt.ylabel('Value')
plt.show()
