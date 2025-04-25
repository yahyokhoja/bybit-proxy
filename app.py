from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        res = requests.get(url)
        data = res.json()
        price = data['result']['list'][0]['lastPrice']
        return jsonify({'price': price})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run()
