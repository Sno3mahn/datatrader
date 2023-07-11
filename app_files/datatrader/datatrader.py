import pandas as pd
import streamlit as st
from numerize.numerize import numerize
import requests
import json
import plotly.graph_objects as go
import dt.streamlit


def send_request(selected_comp):
    try:
        url = 'http://127.0.0.1:5000/data'
        payload = {'text': selected_comp}
        response = requests.post(url, data=payload)
        # print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
def get_forecast(selected_comp):
    try:
        url = 'http://127.0.0.1:5000/forecast'
        payload = {'text': selected_comp}
        response = requests.post(url, data=payload)
        # print(response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
def plot_graphs(act, selected_comp):
    
    fcast_json = json.loads(get_forecast(selected_comp)['data'])
    forecast = pd.DataFrame(data = fcast_json['data'], columns = fcast_json['columns'])
    forecast.index = pd.to_datetime(fcast_json['index'])
    
    # Assuming `df` is the Pandas DataFrame containing the data
    df = forecast
    # Extract the x-values
    x = df.ds

    # Extract the upper and lower limits
    upper_limit = df['yhat_upper']
    lower_limit = df['yhat_lower']

    # Create the trace for the upper limit
    upper = go.Scatter(
        name = 'Upper Limit',
        x=x,
        y=upper_limit,
        mode='lines',
        line=dict(color='lightblue'),
    )

    # Create the trace for the lower limit
    lower = go.Scatter(
        name = 'Lower Limit',
        x=x,
        y=lower_limit,
        mode='lines',
        line=dict(color='red'),
    )

    margin1 = go.Scatter(
        name = 'Estimate',
        x=x,
        y=upper_limit,
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        fill='tonexty'
        )
    
    margin2 = go.Scatter(
        name='Estimate',
        x=x,
        y=lower_limit,
        mode='lines',
        line=dict(color='rgb(246, 23, 26)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        fill='tonexty'
        )

    actual = go.Scatter(
        name = 'Actual Open Price',
        x=act[0],
        y=act[1],
        mode='lines',
        line=dict(color='orange'),
    )

    # Combine the traces
    data = [upper, margin1, margin2, lower, actual]

    # Define the layout
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value'),
        showlegend=True
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Display the plot
    st.write(fig)

    


def main():
    float_formatter = "{:.2f}".format
    del_col = lambda a,b: 'normal' if a>b else 'inverse'

    st.set_page_config(page_title = 'DataTrader')
    st.markdown("<h1 style='text-align: center; color: white;'>DATATRADER</h1>", unsafe_allow_html=True)

    companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'WFC']

    selected_comp = st.selectbox("Select the Company", companies)
    
    if st.button('Submit'):
        
        df_json = json.loads(send_request(selected_comp)['data'])
        data = pd.DataFrame(data = df_json['data'], columns = df_json['columns'])
        data.index = pd.to_datetime(df_json['index'])
        placeholder = st.empty()
        
        with placeholder.container():
            
            kpi1, kpi2, kpi3 = st.columns(3)

            kpi1.metric(
                label = 'Today\'s Open',
                value = float_formatter(data.Open[-1]),
                delta = float_formatter(data.Open[-1] - data.Open[-2]),
            )
            
            kpi2.metric(
                label = 'Yesterday\'s Close',
                value = float_formatter(data.Close[-1]),
                delta = float_formatter(data.Open[-1] - data.Close[-2])
            )
            
            kpi3.metric(
                label = 'Volume',
                value = numerize(int(data.Volume[-1])),
                delta = numerize(int(data.Volume[-1] - data.Volume[-2]))
            )
        
        

        st.markdown('### Open Values of '+selected_comp)
        plot_graphs([data.index, data.Open], selected_comp)
        
application = dt.streamlit.Streamlit()

def __app_main__():
    return application    

if __name__ == '__main__':
    main()

# for i in range(200):
#     new_price = data.Open[-1] + random.rand() * random.choice(range(1,5))
        
#     last_date = data.Open.sort_index().idxmax()
#     date_obj = last_date + timedelta(days=1)
#     next_date = date_obj.strftime('%Y-%m-%d')
    
#     new_row = pd.Series([new_price], index=pd.to_datetime([next_date]))
#     col1 = st.columns(2)
#     with col1[0]:
#         fig = px.line(data.Open.append(new_row))
#         st.write(fig)
#     time.sleep(2)
