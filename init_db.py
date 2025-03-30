import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Insert Users
cur.execute("INSERT INTO users (email, balance, password) VALUES (?, ?, ?)", 
            ('alice@example.com', 5000.00, 'hashed_password_1'))
cur.execute("INSERT INTO users (email, balance, password) VALUES (?, ?, ?)", 
            ('bob@example.com', 3000.50, 'hashed_password_2'))
cur.execute("INSERT INTO users (email, balance, password) VALUES (?, ?, ?)", 
            ('charlie@example.com', 10000.75, 'hashed_password_3'))

# Insert Stocks
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('AAPL', 'Apple Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('GOOGL', 'Alphabet Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('TSLA', 'Tesla Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('NDAQ', 'Nasdaq Inc.'))            
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('MSFT', 'Microsoft Corp.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('META', 'Meta Plaforms, Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('AVGO', 'Broadcom Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('V', 'Visa Inc.'))
cur.execute("INSERT INTO stocks (ticker, full_name) VALUES (?, ?)", 
            ('COST', 'Costco Wholesale Corp.'))



# Insert Purchases
cur.execute("INSERT INTO purchases (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (1, 1, 145.67, '2024-02-23 10:30:00', 2, 0))
cur.execute("INSERT INTO purchases (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (2, 2, 2780.25, '2024-02-23 11:15:00', 3, 0))
cur.execute("INSERT INTO purchases (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (3, 3, 865.50, '2024-02-23 12:00:00', 1, 1))

# Insert Sells
cur.execute("INSERT INTO sells (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (1, 2, 2800.75, '2024-02-23 13:45:00', 3, 0))
cur.execute("INSERT INTO sells (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (2, 3, 870.00, '2024-02-23 14:20:00', 1, 0))
cur.execute("INSERT INTO sells (user_id, stock_id, price, datetime, fullfilled_by_id, is_canceled) VALUES (?, ?, ?, ?, ?, ?)", 
            (3, 1, 150.30, '2024-02-23 15:00:00', 2, 1))

# Insert Currency
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)", 
            ('US Dollar', 'USD', 1.0))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)", 
            ('Euro', 'EUR', 0.85))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)", 
            ('British Pound', 'GBP', 0.75))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)", 
            ('Japanese Yen', 'JPY', 110.0))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)", 
            ('Canadian Dollar', 'CAD', 1.25))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)",
            ('Australian Dollar', 'AUD', 1.35))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)",
            ('Swiss Franc', 'CHF', 0.92))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)",
            ('Chinese Yuan', 'CNY', 6.5))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)",
            ('Indian Rupee', 'INR', 74.0))
cur.execute("INSERT INTO currency (currency_name, currency_name, conversion_rate, converted_price) VALUES (?, ?, ?)",
            ('Singapore Dollar', 'SGD', 1.35))

connection.commit()
connection.close()