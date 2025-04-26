import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        res = requests.get(url)
        if res.status_code != 200:
            return jsonify({'error': f'Ошибка при запросе к API Bybit: {res.status_code}'})
        
        data = res.json()
        tickers = data.get('result', {}).get('list', [])
        if not tickers:
            return jsonify({'error': 'Пустой список тикеров'})
        
        price = tickers[0].get('lastPrice', 'неизвестно')
        return jsonify({'price': price})
    except Exception as e:
        import traceback
        traceback.print_exc()  # добавим вывод ошибки в логи
        return jsonify({'error': f"Ошибка: {str(e)}"})



@app.route('/')
def index():
    return '🚀 Прокси-сервер Bybit работает!'

# Тестовый маршрут API
@app.route('/test')
def test():
    return {'message': 'API работает ✅'}

# Страница для отображения курса
@app.route('/narh')
def narh():
    try:
        # Запрос к вашему прокси-серверу для получения курса
        res = requests.get("https://bybit-proxy-ehep.onrender.com/price")
        price = res.json().get("price", "неизвестно")
    except Exception as e:
        price = "ошибка: " + str(e)

    return render_template("narh.html", price=price)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
