import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def login_session(client):
    with client.session_transaction() as session:
        session['_user_id'] = '1'

def test_purchase_redirects_if_not_logged_in(client):
    response = client.get('/purchase')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_purchase_page_loads(client):
    login_session(client)
    response = client.get('/purchase')
    assert response.status_code == 200
    assert b'Purchase Stock' in response.data

def test_submit_purchase_invalid_balance(client):
    login_session(client)

    response = client.post('/purchase', data={
        'ticker': 'AAPL',
        'shares': 100,
        'price': 100
    }, follow_redirects=True)

    assert b'User Has No Enough Money!' in response.data

def test_submit_purchase_successful(client):
    login_session(client)
    
    response = client.post('/purchase', data={
        'ticker': 'GOOGL',
        'shares': 10,
        'price': 1
    }, follow_redirects=True)

    assert b'Your Purchase Order Has Been Placed' in response.data
    assert b'GOOGL' in response.data
    
def test_cancel_purchase_success(client):
    login_session(client)
    conn = __import__('helper.db_connector').db_connector.get_db_connection()

    # Set up user and stock
    conn.execute("INSERT OR IGNORE INTO users (id, email, balance, password) VALUES (1, 'cancel_user@example.com', 100, 'pw')")
    conn.execute("INSERT OR IGNORE INTO stocks (id, ticker, full_name) VALUES (2, 'MSFT', 'Microsoft Corp')")
    # Set up a purchase
    conn.execute("INSERT INTO purchases (user_id, stock_id, price, fullfilled_by_id, is_canceled) VALUES ( 1, 2, 50, NULL, 0)")
    conn.commit()

    response = client.post('/purchase_cancel/1', follow_redirects=True)
    assert response.status_code == 200


def test_cancel_purchase_invalid(client):
    login_session(client)
    conn = __import__('helper.db_connector').db_connector.get_db_connection()

    response = client.post('/purchase_cancel/999999', follow_redirects=True)
    assert b'Purchase Might Be Fullfilled Already!' in response.data