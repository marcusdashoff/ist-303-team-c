from flask import Blueprint, render_template, request, redirect, url_for, flash
from helper.db_connector import get_db_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

purchase_controller = Blueprint('purchase', __name__)

@purchase_controller.route('/purchase', methods=['POST', 'GET'])
def purchase():
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    tickers = conn.execute('SELECT ticker, full_name FROM stocks').fetchall()
    
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        shares = request.form.get('shares')
        price = request.form.get('price')
        
        # force to reload user
        user = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
        stock = conn.execute('SELECT * FROM stocks WHERE ticker = ?', (ticker,)).fetchone()
        
        total = float(price) * int(shares)
        if user['balance'] >= total:
            for _ in range(int(shares)):
                conn.execute(
                    'INSERT INTO purchases (user_id, stock_id, price, fullfilled_by_id) VALUES (?, ?, ?, ?)',
                    (current_user.id, stock['id'], price, current_user.id)
                )

            conn.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (total, current_user.id))
            
            conn.commit()
            flash('Your Purchase Order Has Been Placed', 'success')
        else:
            flash('User Has No Enough Money!', 'danger')
        
        return redirect(
                url_for('purchase.purchase' )
            )

    return render_template('purchase.html', tickers=tickers, user=current_user)