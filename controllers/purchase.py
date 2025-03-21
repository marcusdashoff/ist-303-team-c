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
                    'INSERT INTO purchases (user_id, stock_id, price) VALUES (?, ?, ?)',
                    (current_user.id, stock['id'], price)
                )

            conn.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (total, current_user.id))
            
            conn.commit()
            flash('Your Purchase Order Has Been Placed', 'success')
        else:
            flash('User Has No Enough Money!', 'danger')
        
        return redirect(
                url_for('purchase.purchase' )
            )

    user_pending_purchases = conn.execute(
        '''
        SELECT p.id, s.ticker, s.full_name, p.price, p.datetime 
        FROM purchases p
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.user_id = ? AND p.fullfilled_by_id IS NULL AND p.is_canceled = 0
        ORDER BY p.datetime DESC
        ''', 
        (current_user.id,)
    ).fetchall()

    return render_template('purchase.html', tickers=tickers, user=current_user, user_pending_purchases=user_pending_purchases)


@purchase_controller.route('/purchase_cancel/<int:purchase_id>', methods=['POST'])
def purchase_cancel(purchase_id):
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # for safety! also pass in user id and ensure fulfillment is not completed!
    to_be_canceled = conn.execute(
        'SELECT * FROM purchases WHERE id = ? AND user_id = ? AND fullfilled_by_id IS NULL AND is_canceled = 0',
        (purchase_id, current_user.id)
    ).fetchone()
    
    if to_be_canceled:
        # Refund the purchase value to the user's balance
        conn.execute(
            'UPDATE users SET balance = balance + ? WHERE id = ?',
            (to_be_canceled['price'], current_user.id)
        )

        # Delete the purchase row
        conn.execute('UPDATE purchases SET is_canceled = 1 WHERE id = ?', (purchase_id,))
        conn.commit()
        
        flash('Purchase Cancellation Succeeded!', 'success')
    else:
        flash('Purchase Might Be Fullfilled Already!', 'danger')

    return redirect(url_for('purchase.purchase'))
    
    
