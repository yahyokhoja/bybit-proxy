import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/price')
def get_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()

        data = res.json()
        tickers = data.get('result', {}).get('list', [])
        if not tickers:
            return jsonify({'error': 'Пустой список тикеров'})

        price = tickers[0].get('lastPrice')
        if price is None:
            return jsonify({'error': 'Поле lastPrice не найдено'})

        return jsonify({'price': price})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Ошибка запроса: {str(e)}'})
    except Exception as e:
        return jsonify({'error': f'Ошибка обработки данных: {str(e)}'})



@app.route('/')
def index():
    return '🚀 Прокси-сервер Bybit работает!'

# Тестовый маршрут API
@app.route('/test')
def test():
    return {'message': 'API работает ✅'}



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
