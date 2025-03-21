DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS stocks;
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL
);

DROP TABLE IF EXISTS purchases;
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    price REAL NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    fullfilled_by_id INTEGER,
    is_canceled BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE,
    FOREIGN KEY (fullfilled_by_id) REFERENCES users(id) ON DELETE SET NULL
);

DROP TABLE IF EXISTS sells;
CREATE TABLE sells (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    stock_id INTEGER NOT NULL,
    price REAL NOT NULL,
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    fullfilled_by_id INTEGER,
    is_canceled BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (stock_id) REFERENCES stocks(id) ON DELETE CASCADE,
    FOREIGN KEY (fullfilled_by_id) REFERENCES users(id) ON DELETE SET NULL
);