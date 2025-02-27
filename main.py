import sqlite3
from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnop'
login_manager = LoginManager()
login_manager.init_app(app)

# TODO: move it to model file!!!!!
class User:
    def __init__(self, user_from_db):
        self.id = user_from_db['id']
        self.email = user_from_db['email']
        self.password = user_from_db['password']
        self.balance = user_from_db['balance']
        if user_from_db['id']:
            self.is_authenticated = True
        else: 
            self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
        
    def get_id(self):
        return str(self.id)


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