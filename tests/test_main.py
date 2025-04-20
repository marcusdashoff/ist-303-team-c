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