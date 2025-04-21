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

def test_index_redirects_if_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']

def test_index_page_loads(client):
    login_session(client)
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Welcome, U made it~" in html
    assert "alice@example.com" in html
    assert "💰💰Account Balance💰💰" in html
    assert "📈📈Current Stock Holdings📈📈" in html
    assert "Past Fulfillment Ledgers" in html

def test_index_displays_holdings_and_transactions(client):
    login_session(client)
    response = client.get('/')
    html = response.get_data(as_text=True)

    # from init_db: alice owns AAPL and GOOGL, sold TSLA
    assert "AAPL" in html
    assert "GOOGL" in html
    assert "Sell" in html or "Buy" in html

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert "Login" in response.get_data(as_text=True)

def test_login_post_success_then_log_out(client):
    response = client.post('/login', data={'username': 'alice@example.com', 'password': 'hashed_password_1'}, follow_redirects=True)
    assert response.status_code == 200
    assert "Welcome, U made it~" in response.get_data(as_text=True)
    
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200

def test_login_post_failure(client):
    response = client.post('/login', data={'username': 'alice@example.com', 'password': 'wrong_password'})
    assert response.status_code == 200
    assert "Invalid credentials" in response.get_data(as_text=True)

def test_logout(client):
    login_session(client)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert "Login" in response.get_data(as_text=True) or "Invalid credentials" in response.get_data(as_text=True)