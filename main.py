from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User
from controllers.search import search_controller
from controllers.purchase import purchase_controller
from controllers.sell import sell_controller
from helper.db_connector import get_db_connection
from apscheduler.schedulers.background import BackgroundScheduler
from jobs.fulfillment import fulfill_order

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnop'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(search_controller)
app.register_blueprint(purchase_controller)
app.register_blueprint(sell_controller)

scheduler = BackgroundScheduler()
scheduler.add_job(func=fulfill_order, trigger="interval", seconds=15)
scheduler.start()

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return User(user)

@app.route('/')
#@login_required
def index():
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    
    conn = get_db_connection()

    # refresh balance!
    user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()

    holdings = conn.execute('''
        SELECT us.shares, s.ticker, s.full_name
        FROM user_stock us
        JOIN stocks s ON s.id = us.stock_id
        WHERE us.user_id = ?
    ''', (current_user.id,)).fetchall()
        
    purchases = conn.execute('''
        SELECT s.ticker, p.price, p.datetime
        FROM purchases p
        JOIN sells s2 ON p.fullfilled_by_id = s2.id
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.user_id = ? AND p.fullfilled_by_id IS NOT NULL AND p.is_canceled = 0
    ''', (current_user.id,)).fetchall()

    sells = conn.execute('''
        SELECT s.ticker, s2.price, s2.datetime
        FROM sells s2
        JOIN purchases p ON s2.fullfilled_by_id = p.id
        JOIN stocks s ON s2.stock_id = s.id
        WHERE s2.user_id = ? AND s2.fullfilled_by_id IS NOT NULL AND s2.is_canceled = 0
    ''', (current_user.id,)).fetchall()

    transactions = [
        dict(type="Buy", ticker=row["ticker"], price=row["price"], datetime=row["datetime"])
        for row in purchases
    ] + [
        dict(type="Sell", ticker=row["ticker"], price=row["price"], datetime=row["datetime"])
        for row in sells
    ]

    # make sure its by date time descending
    transactions.sort(key=lambda x: x["datetime"], reverse=True)

    return render_template(
        'index.html',
        user=user,
        holdings=holdings,
        transactions=transactions
    )

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
    
