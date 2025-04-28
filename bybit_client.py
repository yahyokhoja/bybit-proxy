import requests
import time
import hmac
import hashlib

# Настройки API
BASE_URL = "https://api.bybit.com"

def sign(api_secret, params):
    """Создание подписи для запросов"""
    param_str = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
    return hmac.new(api_secret.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha256).hexdigest()

def check_keys(api_key, api_secret):
    """Проверка валидности API ключей через запрос баланса"""
    try:
        timestamp = str(int(time.time() * 1000))
        params = {
            "timestamp": timestamp,
            "api_key": api_key,
        }
        params["sign"] = sign(api_secret, params)

        response = requests.get(f"{BASE_URL}/v2/private/wallet/balance", params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['ret_code'] == 0:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Ошибка проверки ключей: {e}")
        return False

def get_market_data():
    """Просто получить информацию о рынке"""
    try:
        response = requests.get(f"{BASE_URL}/v2/public/tickers")
        return response.json()
    except Exception as e:
        print(f"Ошибка получения маркет данных: {e}")
        return None

def place_order(api_key, api_secret, side, qty, price):
    """Создать ордер"""
    try:
        timestamp = str(int(time.time() * 1000))
        params = {
            "api_key": api_key,
            "symbol": "BTCUSDT",
            "side": side,
            "order_type": "Limit",
            "qty": qty,
            "price": price,
            "time_in_force": "GoodTillCancel",
            "timestamp": timestamp,
        }
        params["sign"] = sign(api_secret, params)

        response = requests.post(f"{BASE_URL}/v2/private/order/create", data=params)
        data = response.json()
        if data['ret_code'] == 0:
            return "Ордер успешно создан!"
        else:
            return f"Ошибка: {data.get('ret_msg', 'Неизвестная ошибка')}"
    except Exception as e:
        return f"Ошибка создания ордера: {e}"

def get_balance(api_key, api_secret):
    """Получить баланс"""
    try:
        timestamp = str(int(time.time() * 1000))
        params = {
            "api_key": api_key,
            "timestamp": timestamp,
        }
        params["sign"] = sign(api_secret, params)

        response = requests.get(f"{BASE_URL}/v2/private/wallet/balance", params=params)
        data = response.json()
        if data['ret_code'] == 0:
            return data['result']
        else:
            return {}
    except Exception as e:
        print(f"Ошибка получения баланса: {e}")
        return {}
