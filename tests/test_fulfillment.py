import pytest
import sys
import os
import subprocess
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from jobs.fulfillment import fulfill_order
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def reset_db():
    # https://stackoverflow.com/questions/68666464/how-to-use-pytest-with-subprocess
    subprocess.run(["python3", "init_db.py"], check=True)

def test_fulfill_order_match_found():
    reset_db()

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    # mark all unfilfilled as canceled for now!
    cur.execute("UPDATE purchases SET is_canceled = 1 WHERE fullfilled_by_id IS NULL")
    cur.execute("UPDATE sells SET is_canceled = 1 WHERE fullfilled_by_id IS NULL")

    cur.execute("INSERT INTO purchases (user_id, stock_id, price, is_canceled) VALUES (?, ?, ?, ?)", (3, 3, 900, 0))
    cur.execute("INSERT INTO sells (user_id, stock_id, price, is_canceled) VALUES (?, ?, ?, ?)", (1, 3, 850, 0))
    conn.commit()

    fulfill_order()

    updated_purchase = cur.execute("SELECT * FROM purchases WHERE user_id = 3 AND stock_id = 3 ORDER BY id DESC").fetchone()
    updated_sell = cur.execute("SELECT * FROM sells WHERE user_id = 1 AND stock_id = 3 ORDER BY id DESC").fetchone()

    assert updated_purchase['fullfilled_by_id'] == updated_sell['id']
    assert updated_sell['fullfilled_by_id'] == updated_purchase['id']

    charlie_stock = cur.execute("SELECT * FROM user_stock WHERE user_id = 3 AND stock_id = 3").fetchone()
    assert charlie_stock is not None and charlie_stock['shares'] >= 1

    charlie = cur.execute("SELECT * FROM users WHERE id = 3").fetchone()
    alice = cur.execute("SELECT * FROM users WHERE id = 1").fetchone()

    assert round(charlie['balance'], 2) == 10050.75
    assert round(alice['balance'], 2) == round(5000.00 + 850, 2)

    conn.close()

def test_fulfill_order_no_match():
    reset_db()

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("INSERT INTO purchases (user_id, stock_id, price, is_canceled) VALUES (?, ?, ?, ?)", (2, 3, 100, 0))
    conn.commit()

    fulfill_order()

    updated = cur.execute("SELECT * FROM purchases WHERE user_id = 2 AND stock_id = 3 ORDER BY id DESC").fetchone()
    assert updated['fullfilled_by_id'] is None

    conn.close()