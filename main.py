from flask import Flask, render_template, redirect, url_for, request, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User
from controllers.search import search_controller
from helper.db_connector import get_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdefghijklmnop'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(search_controller)

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
    
