# import yfinance as yf
# import pandas as pd
# import matplotlib.pyplot as plt
# from prophet import Prophet
# from prophet.serialize import model_to_json


# companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'WFC']
# data = yf.download(tickers = companies,
#             period = "6y",
#             interval = "1d",
#             prepost = False,
#             repair = True) 

# df = pd.DataFrame(columns=['ds', 'y'])

# df['ds'] = pd.to_datetime(data.index)
# df['y'] = data['Open']['WFC'].values

# m = Prophet()
# m.add_seasonality(name='quarterly', period=91.5, fourier_order=8)
# m.fit(df)
# future = m.make_future_dataframe(periods=200)

# forecast = m.predict(future)


# with open('WFC.json', 'w') as fout:
#     fout.write(model_to_json(m))  # Save model


# fig = m.plot_components(forecast)

# plt.figure(figsize=(15, 7))
# plt.plot(forecast['ds'], forecast['yhat_upper'], color='lightblue')
# plt.plot(forecast['ds'], forecast['yhat_lower'], color='lightblue')
# plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=1)
# plt.plot(forecast['ds'], forecast['yhat'], color='blue')
# plt.plot(data.Open.AAPL,color='green')
# plt.xlabel('Time (years)')
# plt.ylabel('Value')
# plt.show()


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from prophet.serialize import model_to_json


def func():
    companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'WFC']
    data = yf.download(tickers = companies,
                period = "6y",
                interval = "1d",
                prepost = False,
                repair = True) 

    for i in companies:

        df = pd.DataFrame(columns=['ds', 'y'])

        df['ds'] = pd.to_datetime(data.index)
        df['y'] = data['Open'][i].values

        m = Prophet()
        m.add_seasonality(name='quarterly', period=91.5, fourier_order=8)
        m.fit(df)
        future = m.make_future_dataframe(periods=200)

        forecast = m.predict(future)

        with open(rf'app_files\datatrader_services\{i}.json', 'w') as fout:
            fout.write(model_to_json(m))  # Save model

        fig = m.plot_components(forecast)

        plt.figure(figsize=(15, 7))
        plt.plot(forecast['ds'], forecast['yhat_upper'], color='lightblue')
        plt.plot(forecast['ds'], forecast['yhat_lower'], color='lightblue')
        plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='lightblue', alpha=1)
        plt.plot(forecast['ds'], forecast['yhat'], color='blue')
        plt.plot(data.Open.AAPL,color='green')
        plt.xlabel('Time (years)')
        plt.ylabel('Value')
        plt.show()
        
func()