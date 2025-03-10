import pytest
import sys
sys.path.insert(0, '/Users/stone/src/ist-303-team-c')
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_redirects_if_not_logged_in(client):
    response = client.get('/search')
    # well no flask login, do redirect then~
    assert response.status_code == 302
    assert "/login" in response.headers['Location']

def test_search_page_loads(client):
    # hijack session to pretend we logged in~~~
    with client.session_transaction() as session:
        session['_user_id'] = '1'  
    
    response = client.get('/search')
    assert response.status_code == 200
    assert response.get_data(as_text=True).find("Yoooo, search stock here") != -1

def test_search_returns_result(client):
    # hijack session to pretend we logged in~~~
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    
    response = client.post('/search', data={'ticker': 'AAPL'})
    assert response.status_code == 200
    assert response.get_data(as_text=True).find("AAPL") != -1
    assert response.get_data(as_text=True).find("Company Name") != -1
    assert response.get_data(as_text=True).find("Current Price") != -1
    assert response.get_data(as_text=True).find("Historical High") != -1
    assert response.get_data(as_text=True).find("Historical Low") != -1
    assert response.get_data(as_text=True).find("Trade Volume within 24 hrs") != -1

def test_search_not_found(client):
    # hijack session to pretend we logged in~~~
    with client.session_transaction() as session:
        session['_user_id'] = '1'
    
    response = client.post('/search', data={'ticker': 'HODL'})
    assert response.status_code == 200
    assert response.get_data(as_text=True).find("Woow I What Ya Tryna Search") != -1