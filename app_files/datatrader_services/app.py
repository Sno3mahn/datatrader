from flask import Flask, request, jsonify
import yfinance as finance
from prophet.serialize import model_from_json
from os.path import abspath

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def fetch_data():

    company = request.form['text']
    data = finance.download(tickers = company,
            period = "6y",
            interval = "1d",
            prepost = False,
            repair = True)   
    
    return jsonify(data = data.to_json(orient='split', date_format='iso'))

@app.route('/forecast', methods=['POST'])
def forecast_data():

    company = request.form['text']
    with open(abspath(f'{company}.json'), 'r') as fin:
        m = model_from_json(fin.read())  # Load model 
    future = m.make_future_dataframe(periods=200)
    forecast = m.predict(future)
    
    return jsonify(data = forecast.to_json(orient='split', date_format='iso'))

if __name__ == '__main__':
    app.run(debug=True)
    
def __service_main__(port):
	app.run('0.0.0.0', port=int(port), debug=False)
