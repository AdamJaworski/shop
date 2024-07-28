"""
session_hash TEXT,
item_id INTEGER,
amount INTEGER
"""

from app.model.database_decorators import *


@get_from_database
def get_user_cart(cursor, user_hash):
    cursor.execute('SELECT item_id, amount FROM cart WHERE session_hash = ?', (user_hash,))
    return cursor.fetchall()


@on_database_operation
def add_to_cart(cursor, item_id, amount, user_hash):
    cursor.execute('INSERT INTO cart (session_hash, item_id, amount) VALUES (?, ?, ?)', (user_hash, item_id, amount))