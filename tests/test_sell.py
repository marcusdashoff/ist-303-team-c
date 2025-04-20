import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from helper.db_connector import get_db_connection


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def login_session(client):
    with client.session_transaction() as session:
        session['_user_id'] = '1'

def test_sell_redirects_if_not_logged_in(client):
    response = client.get('/sell')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_sell_page_loads(client):
    login_session(client)

    response = client.get('/sell')
    assert response.status_code == 200
    assert b'Sell Stocks' in response.data

def test_submit_sell_successful(client):
    login_session(client)

    response = client.post('/sell', data={
        'shares': 2,
        'price': 0.01,
        'submit_stock': 2,
        'stock_id': 2
    }, follow_redirects=True)

    assert b'Your sell order has been placed!' in response.data
    
    conn = get_db_connection()
    sells = conn.execute("SELECT * FROM sells WHERE user_id = 1 AND stock_id = 2 AND price = 0.01").fetchall()
    assert len(sells) == 2 

    user_stock = conn.execute("SELECT shares FROM user_stock WHERE user_id = 1 AND stock_id = 2").fetchone()
    assert user_stock is not None
    assert user_stock['shares'] < 58 

def test_cancel_sell_success(client):
    login_session(client)
    conn = get_db_connection()
    
    test_insert = conn.execute(
        'INSERT INTO sells (user_id, stock_id, price) VALUES (?, ?, ?)',
        (1, 2, 0.01)
    )
    new_sell_id = test_insert.lastrowid

    response = client.post('/sell_cancel/' + str(new_sell_id), follow_redirects=True)
    assert response.status_code == 200

def test_cancel_sell_invalid(client):
    login_session(client)

    response = client.post('/sell_cancel/99999', follow_redirects=True)
    assert 'Sell Might Be Fullfilled Already!' in response.get_data(as_text=True)