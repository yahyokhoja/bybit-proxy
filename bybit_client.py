import requests
import time
import hmac
import hashlib

API_URL = "https://api.bybit.com"

def get_signature(api_secret, params):
    sorted_params = sorted(params.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    return hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_market_data():
    try:
        response = requests.get(f"{API_URL}/v5/market/tickers?category=linear")
        if response.status_code == 200:
            return response.json().get('result', {}).get('list', [])
    except Exception as e:
        print("Ошибка получения данных:", e)
    return []

def place_order(api_key, api_secret, side, qty, price):
    endpoint = "/v5/order/create"
    url = API_URL + endpoint
    timestamp = str(int(time.time() * 1000))
    params = {
        "category": "linear",
        "symbol": "BTCUSDT",
        "side": side.upper(),
        "orderType": "LIMIT",
        "qty": qty,
        "price": price,
        "timeInForce": "GTC",
        "timestamp": timestamp,
        "api_key": api_key,
    }
    sign = get_signature(api_secret, params)
    headers = {
        "X-BYBIT-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    params["sign"] = sign
    try:
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:
            return "Ордер успешно размещен!"
        else:
            return f"Ошибка размещения ордера: {response.text}"
    except Exception as e:
        return f"Ошибка: {e}"

def get_balance(api_key, api_secret):
    endpoint = "/v5/account/wallet-balance"
    url = API_URL + endpoint
    timestamp = str(int(time.time() * 1000))
    params = {
        "accountType": "UNIFIED",
        "timestamp": timestamp,
        "api_key": api_key,
    }
    sign = get_signature(api_secret, params)
    headers = {
        "X-BYBIT-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    params["sign"] = sign
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json().get('result', {}).get('list', [])
        else:
            return f"Ошибка получения баланса: {response.text}"
    except Exception as e:
        return f"Ошибка: {e}"
