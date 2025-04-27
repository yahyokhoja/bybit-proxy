import time
import hashlib
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import threading
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Это важно для работы с сессиями

# Переменные для хранения состояния
bot_running = False
api_key = None
api_secret = None

# Функция для старта бота
def start_bot():
    global bot_running
    while bot_running:
        # Использование API-ключей для торговли на Bybit
        if api_key and api_secret:
            try:
                data = get_bybit_data(api_key, api_secret)
                print("Bot is running with API Key:", api_key)
                print("Bybit API response:", data)
            except Exception as e:
                print(f"Error fetching data from Bybit: {e}")
        # Пауза между запросами (например, раз в минуту)
        time.sleep(60)

# Получение данных с Bybit API (пример)
def get_bybit_data(api_key, api_secret):
    url = "https://api.bybit.com/v2/public/time"
    params = {
        'api_key': api_key,
        'timestamp': str(int(time.time() * 1000)),
    }
    
    # Генерация подписи для запроса
    params['sign'] = generate_signature(params, api_secret)
    
    response = requests.get(url, params=params)
    
    # Проверка на успешный ответ от API
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Bybit API error: {response.status_code}, {response.text}")

# Генерация подписи для API-запроса
def generate_signature(params, api_secret):
    sorted_params = sorted(params.items())
    param_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
    signature = hashlib.sha256((param_string + f"&api_secret={api_secret}").encode('utf-8')).hexdigest()
    return signature

# Главная страница
@app.route('/')
def index():
    return render_template('index.html', bot_running=bot_running)

# Страница для ввода API-ключа
@app.route('/set_api_keys', methods=['POST'])
def set_api_keys():
    global api_key, api_secret
    api_key = request.form['api_key']
    api_secret = request.form['api_secret']
    
    # Сохраняем ключи в сессии для последующего использования
    session['api_key'] = api_key
    session['api_secret'] = api_secret
    
    return redirect(url_for('index'))

# Страница для запуска/остановки бота
@app.route('/toggle_bot', methods=['POST'])
def toggle_bot():
    global bot_running
    if bot_running:
        bot_running = False
    else:
        bot_running = True
        threading.Thread(target=start_bot, daemon=True).start()  # daemon=True позволяет завершить поток при завершении основного процесса
    return jsonify({"status": "running" if bot_running else "stopped"})

if __name__ == "__main__":
    app.run(debug=True)
