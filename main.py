import sqlite3
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnop'
login_manager = LoginManager()
login_manager.init_app(app)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return User(user)

@app.route('/')
#@login_required
def index():
    if current_user and current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return redirect(url_for('login'))

# https://flask-login.readthedocs.io/en/latest/
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (request.form['username'],)).fetchone()
        if user and user['password'] == request.form['password']: # todo: encrypt passwords
            login_user(User(user))
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user and current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    
@app.route('/search', methods=('GET', 'POST'))
def search():
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    if request.method == 'POST':
        ticker = request.form['ticker']
        conn = get_db_connection()
        stock = conn.execute('SELECT * FROM stocks WHERE ticker = ?', (ticker,)).fetchone()
        current_price = conn.execute('SELECT price FROM sells INNER JOIN stocks ON (stocks.id = stock_id) WHERE ticker = ? ORDER BY datetime DESC LIMIT 1', (ticker,)).fetchone()
        historical_high = conn.execute('SELECT MAX(price) as price FROM sells INNER JOIN stocks ON (stocks.id = stock_id) WHERE ticker = ?', (ticker,)).fetchone()
        historical_low = conn.execute('SELECT MIN(price) as price FROM sells INNER JOIN stocks ON (stocks.id = stock_id) WHERE ticker = ?', (ticker,)).fetchone()
        trading_volume_with_past_24_hours = conn.execute(
            'SELECT SUM(price) as price FROM sells INNER JOIN stocks ON (stocks.id = stock_id) WHERE ticker = ? AND datetime >= datetime("now", "-24 hours")', 
            (ticker,)).fetchone()
        
        if stock:
            return render_template('search.html', 
                                   user=current_user, 
                                   stock=stock, 
                                   current_price=current_price, 
                                   historical_high=historical_high, 
                                   historical_low=historical_low,
                                   trading_volume_with_past_24_hours=trading_volume_with_past_24_hours
                                   )
        else:
            return render_template('search.html', user=current_user, error='Woow I What Ya Tryna Search')
    return render_template('search.html', user=current_user)
    
