from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import bybit_client  # подключаем твой код

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # замени на что-то более безопасное
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['api_key'] = request.form['api_key']
        session['api_secret'] = request.form['api_secret']
        return redirect(url_for('market'))
    return render_template('index.html')

@app.route('/market')
def market():
    if 'api_key' not in session:
        return redirect(url_for('index'))
    data = bybit_client.get_market_data()
    return render_template('market.html', data=data)

@app.route('/trade', methods=['GET', 'POST'])
def trade():
    if 'api_key' not in session:
        return redirect(url_for('index'))
    message = ''
    if request.method == 'POST':
        side = request.form['side']
        qty = request.form['qty']
        price = request.form['price']
        message = bybit_client.place_order(session['api_key'], session['api_secret'], side, qty, price)
    return render_template('trade.html', message=message)

@app.route('/balance')
def balance():
    if 'api_key' not in session:
        return redirect(url_for('index'))
    balance = bybit_client.get_balance(session['api_key'], session['api_secret'])
    return render_template('balance.html', balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
