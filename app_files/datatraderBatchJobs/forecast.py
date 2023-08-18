import yfinance as yf
import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json
from os.path import abspath, dirname, join
from pathlib import Path 
import dt.user
from dt.cloud.blob_storage import BlobStorage

dt.user.set_current_user(dt.user.signed_user())

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

        model_path = f'{i}.json'
        s3 = BlobStorage() 
        s3.put_object(model_to_json(m).encode(), model_path)
