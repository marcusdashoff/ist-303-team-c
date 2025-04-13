from flask import Blueprint, render_template, request, redirect, url_for
from helper.db_connector import get_db_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

search_controller = Blueprint('search', __name__)

@search_controller.route('/search', methods=['GET', 'POST'])
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
            (ticker,)
        ).fetchone()
        if stock:
            return render_template(
                'search.html',
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