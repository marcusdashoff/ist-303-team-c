from flask import Blueprint, render_template, request, redirect, url_for, flash
from helper.db_connector import get_db_connection
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from types import SimpleNamespace

sell_controller = Blueprint('sell', __name__)

@sell_controller.route('/sell', methods=['POST', 'GET'])
def sell():
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # TODO: add in user stocks table to indicate current holdings + read from that table instead!
    current_holdings = [
        SimpleNamespace(stock_id=1, shares=10, ticker="AAPL", full_name="Apple Inc."),
        SimpleNamespace(stock_id=2, shares=10, ticker="GOOGL", full_name="Alphabet Inc."), 
        SimpleNamespace(stock_id=5, shares=5, ticker="MSFT", full_name="Microsoft Corp.")
    ]
    
    if request.method == 'POST':
        stock_id = request.form.get('submit_stock')  
        shares = int(request.form.get('shares'))
        price = float(request.form.get('price'))

        for _ in range(shares):
            conn.execute(
                'INSERT INTO sells (user_id, stock_id, price) VALUES (?, ?, ?)',
                (current_user.id, stock_id, price)
            )

        conn.commit()
        flash('Your sell order has been placed!', 'success')
        return redirect(url_for('sell.sell'))

    user_pending_sells = conn.execute(
        '''
        SELECT p.id, s.ticker, s.full_name, p.price, p.datetime 
        FROM sells p
        JOIN stocks s ON p.stock_id = s.id
        WHERE p.user_id = ? AND p.fullfilled_by_id IS NULL AND p.is_canceled = 0
        ORDER BY p.datetime DESC
        ''', 
        (current_user.id,)
    ).fetchall()

    return render_template('sell.html', current_holdings=current_holdings, user=current_user, user_pending_sells=user_pending_sells)


@sell_controller.route('/sell_cancel/<int:sell_id>', methods=['POST'])
def sell_cancel(sell_id):
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # for safety! also pass in user id and ensure fulfillment is not completed!
    to_be_canceled = conn.execute(
        'SELECT * FROM sells WHERE id = ? AND user_id = ? AND fullfilled_by_id IS NULL AND is_canceled = 0',
        (sell_id, current_user.id)
    ).fetchone()
    
    if to_be_canceled:
        # TODO: add back stock holding for user

        conn.execute('UPDATE sells SET is_canceled = 1 WHERE id = ?', (sell_id,))
        conn.commit()
        
        flash('Sell Cancellation Succeeded!', 'success')
    else:
        flash('Sell Might Be Fullfilled Already!', 'danger')

    return redirect(url_for('sell.sell'))
    
    
