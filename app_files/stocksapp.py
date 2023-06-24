import streamlit as st
import yfinance as finance

def get_company_ticker(name):
	company = finance.Ticker(name)
	return company

st.markdown("<h1 style='text-align: center; color: white;'>DATATAILR STOCK APP</h1>", unsafe_allow_html=True)

first_company = get_company_ticker("GOOGL")
second_company = get_company_ticker("MSFT")

google = finance.download("GOOGL", start="2022-04-01", end="2022-09-01")
microsoft = finance.download("MSFT", start="2022-04-01", end="2022-09-01")

data1 = first_company.history(period="1mo")
data2 = second_company.history(period="1mo")

st.write("\n\n\n")

st.write("""### Google""")
st.write(first_company.info['longBusinessSummary'])
st.write(google)
st.line_chart(data1.values)

st.write("""### Microsoft""")
st.write(second_company.info['longBusinessSummary'])
st.write(microsoft)
st.line_chart(data2.values)