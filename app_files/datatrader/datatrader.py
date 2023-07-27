import pandas as pd
import streamlit as st
from numerize.numerize import numerize
import requests
import json
import plotly.graph_objects as go
import dt.streamlit
from dt.service import service_host_and_port

# Function to fetch company-wise historical data from a service hosted via datatailr
@st.cache_data
def get_data(selected_comp):
    
    # `DT service` has been hard-coded here, whatever name is used as parameter for service_host_and_port() must be the same when naming the service
    host, port=service_host_and_port('DT service')
    try:
        url = f'http://{host}:{port}/data'
        payload = {'text': selected_comp}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(e)
        return None

# Function to fetch forecast data from service
@st.cache_resource
def get_forecast(selected_comp):
    
    host, port=service_host_and_port('DT service')
    try:
        url = f'http://{host}:{port}/forecast'
        payload = {'text': selected_comp}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
def plot_graphs(actual_price, selected_comp):
    
    # Forecast data is loaded into dataframe 
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
    
    # Shading from upper limit
    margin1 = go.Scatter(
        name = 'Estimate',
        x=x,
        y=upper_limit,
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        fill='tonexty'
        )
    
    # Shading from lower limit
    margin2 = go.Scatter(
        name='Estimate',
        x=x,
        y=lower_limit,
        mode='lines',
        line=dict(color='rgb(246, 23, 26)'),
        fillcolor='rgba(68, 68, 68, 0.2)',
        fill='tonexty'
        )
    
    # Actual price curve
    actual_curve = go.Scatter(
        name = 'Actual Open Price',
        x=actual_price[0],
        y=actual_price[1],
        mode='lines',
        line=dict(color='orange'),
    )

    # Combine the traces
    data = [upper, margin1, margin2, lower, actual_curve]

    # Define the layout
    layout = go.Layout(
        xaxis=dict(title='Date'),
        yaxis=dict(title='Value'),
        showlegend=False
    )

    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Display the plot
    st.write(fig)

def main():
    
    # Format float values to 2 decimal places
    float_formatter = "{:.2f}".format

    # Setting page title, header, etc.
    st.set_page_config(page_title = 'DataTrader')
    st.markdown("<h1 style='text-align: center; color: white;'>DATATRADER</h1>", unsafe_allow_html=True)

    # Companies list; append ticker symbols to the list for more
    companies = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOGL', 'WFC']

    # Drop down menu
    selected_comp = st.selectbox("Select the Company", companies)
    
    if st.button('Submit'):
        
        # Load data from service into dataframe `df`
        df_json = json.loads(get_data(selected_comp)['data'])
        data = pd.DataFrame(data = df_json['data'], columns = df_json['columns'])
        data.index = pd.to_datetime(df_json['index'])
        
        # Section to hold the KPIs
        indicators = st.empty()
        
        with indicators.container():
            
            # Divide the indicator section into 3 columns
            indicator1, indicator2, indicator3 = st.columns(3)
            
            # Display Latest Open Price and delta with last day's
            indicator1.metric(
                label = 'Today\'s Open',
                value = float_formatter(data['Open'][-1]),
                delta = float_formatter(data['Open'][-1] - data['Open'][-2]),
            )
            
            # Display Latest Close Price and delta with last day's
            indicator2.metric(
                label = 'Yesterday\'s Close',
                value = float_formatter(data['Close'][-1]),
                delta = float_formatter(data['Close'][-1] - data['Close'][-2])
            )
            
            # Display Latest Volume Price and delta with last day's
            indicator3.metric(
                label = 'Volume',
                value = numerize(int(data['Volume'][-1])),
                delta = numerize(int(data['Volume'][-1] - data['Volume'][-2]))
            )        
        
        st.markdown('### Open Values of '+selected_comp)
        plot_graphs([data.index, data['Open']], selected_comp)
        st.markdown("- <font color='yellow'>Actual price</font>", unsafe_allow_html=True)
        st.markdown("- <font color='blue'>Maximum estimate</font>", unsafe_allow_html=True)
        st.markdown("- <font color='red'>Minimum estimate</font>", unsafe_allow_html=True)


        # Background information on the plots
        equation1 = r'''
            $$
            y(t) = g(t) + s(t) + h(t) + \epsilon_{t}
            $$'''
        equation2 = r'''
                $$
                s(t) = \sum_{n=1}^N ( a_{n} cos( \frac{n!}{k!(n-k)!} ) + b_{n} sin( \frac{n!}{k!(n-k)!} ) )
                $$'''
        st.divider()
        st.write('Our Forecasting model uses Facebook\'s Prophet library')
        st.write('A decomposable time series model [Harvey & Peters 1990](http://www.stat.yale.edu/~lc436/papers/Harvey_Peters1990.pdf) with three main model components: trend, seasonality, and holidays is used. They are combined in the following equation:')
        st.markdown(equation1)
        st.markdown('- g(t) is the trend function which models non-periodic changes in the value of the time series')
        st.markdown('- s(t) represents periodic changes (e.g., weekly and yearly seasonality)')
        st.markdown('- h(t) represents the effects of holidays')
        st.write('An additional seasonality component is incorporated to model the periodic effects using the Fourier Series equation')
        st.markdown(equation2)
        st.markdown('- P is the regular period, which we have taken as 91.5 to simulate the effect of a quarter')

        
application = dt.streamlit.Streamlit()

def __app_main__():
    return application    

if __name__ == '__main__':
    main()
