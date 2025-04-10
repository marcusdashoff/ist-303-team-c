from helper.db_connector import get_db_connection

def fulfill_order():
    conn = get_db_connection()

    purchases = conn.execute(
        '''
        SELECT * FROM purchases 
        WHERE fullfilled_by_id IS NULL AND is_canceled = 0 
        ORDER BY datetime ASC
        '''
    ).fetchall()

    for purchase in purchases:
        matching_sell = conn.execute(
            '''
            SELECT * FROM sells 
            WHERE fullfilled_by_id IS NULL 
              AND is_canceled = 0 
              AND stock_id = ? 
              AND user_id != ? 
              AND price <= ?
            ORDER BY price ASC, datetime ASC
            LIMIT 1
            ''',
            (purchase['stock_id'], purchase['user_id'], purchase['price'])
        ).fetchone()

        if matching_sell:
            conn.execute(
                'UPDATE purchases SET fullfilled_by_id = ? WHERE id = ?',
                (matching_sell['id'], purchase['id'])
            )
            conn.execute(
                'UPDATE sells SET fullfilled_by_id = ? WHERE id = ?',
                (purchase['id'], matching_sell['id'])
            )

            existing = conn.execute(
                '''
                SELECT * FROM user_stock 
                WHERE user_id = ? AND stock_id = ?
                ''',
                (purchase['user_id'], purchase['stock_id'])
            ).fetchone()

            if existing:
                conn.execute(
                    '''
                    UPDATE user_stock SET shares = shares + 1 
                    WHERE user_id = ? AND stock_id = ?
                    ''',
                    (purchase['user_id'], purchase['stock_id'])
                )
            else:
                conn.execute(
                    '''
                    INSERT INTO user_stock (user_id, stock_id, shares) 
                    VALUES (?, ?, 1)
                    ''',
                    (purchase['user_id'], purchase['stock_id'])
                )

            refund = purchase['price'] - matching_sell['price']
            if refund > 0:
                conn.execute(
                    'UPDATE users SET balance = balance + ? WHERE id = ?',
                    (refund, purchase['user_id'])
                )

            conn.execute(
                'UPDATE users SET balance = balance + ? WHERE id = ?',
                (matching_sell['price'], matching_sell['user_id'])
            )

    conn.commit()
    print("Fulfillment Finished.")
