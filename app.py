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
    

@app.route('/')
def index():
    return '🚀 Прокси-сервер Bybit работает!'

# Можно добавить ещё тестовый маршрут для API
@app.route('/test')
def test():
    return {'message': 'API работает ✅'}


@app.route('/narh')
def narh():
    try:
        res = requests.get("https://bybit-proxy-ehep.onrender.com/price")
        price = res.json().get("price", "неизвестно")
    except:
        price = "ошибка"

    return render_template("narh.html", price=price)



if __name__ == '__main__':
    app.run()
