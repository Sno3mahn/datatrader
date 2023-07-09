import time
from datetime import datetime, timedelta
import yfinance as finance
import pandas as pd
from numpy import random
import plotly.express as px
import streamlit as st
from numerize.numerize import numerize
import dt.streamlit

def main():
    float_formatter = "{:.2f}".format
    del_col = lambda a,b: 'normal' if a>b else 'inverse'

    st.set_page_config(page_title = 'DataTrader')
    st.markdown("<h1 style='text-align: center; color: white;'>DATATRADER</h1>", unsafe_allow_html=True)


    companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'WFC']

    @st.cache_resource
    def fetch_data():
        
        data = finance.download(tickers = companies,
                period = "1y",
                interval = "1d",
                prepost = False,
                repair = True)   
        return data
    data = fetch_data()

    selected_comp = st.selectbox("Select the Company", companies)

    placeholder = st.empty()

    with placeholder.container():
        
        kpi1, kpi2, kpi3 = st.columns(3)

        kpi1.metric(
            label = 'Today\'s Open',
            value = float_formatter(data.Open[selected_comp][-1]),
            delta = float_formatter(data.Open[selected_comp][-1] - data.Open[selected_comp][-2]),
        )
        
        kpi2.metric(
            label = 'Yesterday\'s Close',
            value = float_formatter(data.Close[selected_comp][-1]),
            delta = float_formatter(data.Open[selected_comp][-1] - data.Close[selected_comp][-2])
        )
        
        kpi3.metric(
            label = 'Volume',
            value = numerize(int(data.Volume[selected_comp][-1])),
            delta = numerize(int(data.Volume[selected_comp][-1] - data.Volume[selected_comp][-2]))
        )

    st.markdown('### Open Values of '+selected_comp)
    st.write(px.line(data.Open[selected_comp]))

application = dt.streamlit.Streamlit()

def __app_main__():
    return application

# for i in range(200):
#     new_price = data.Open[selected_comp][-1] + random.rand() * random.choice(range(1,5))
        
#     last_date = data.Open[selected_comp].sort_index().idxmax()
#     date_obj = last_date + timedelta(days=1)
#     next_date = date_obj.strftime('%Y-%m-%d')
    
#     new_row = pd.Series([new_price], index=pd.to_datetime([next_date]))
#     col1 = st.columns(2)
#     with col1[0]:
#         fig = px.line(data.Open[selected_comp].append(new_row))
#         st.write(fig)
#     time.sleep(2)
