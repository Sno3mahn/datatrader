from flask import Flask, request, jsonify
import yfinance as finance
from prophet.serialize import model_from_json
from os.path import abspath, dirname, join
import io

import dt.user
from dt.cloud.blob_storage import BlobStorage

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

    dt.user.set_current_user(dt.user.signed_user())

    s3 = BlobStorage()

    company = request.form['text']

    file_name = company+".json"

    encoded_file = io.BytesIO(s3.get_object(file_name))
   
    m = model_from_json(encoded_file.read().decode())  # Load model 

    future = m.make_future_dataframe(periods=200)

    forecast = m.predict(future)
    
    return jsonify(data = forecast.to_json(orient='split', date_format='iso'))

if __name__ == '__main__':
    app.run(debug=False)
    
def __service_main__(port):
	app.run('0.0.0.0', port=int(port), debug=False)
