"""
user_cookie TEXT
item_id INTEGER foreign key (items)
amount INTEGER
"""

from app.model.database_decorators import *


@get_from_database
def get_user_cart(cursor, user_id):
    cursor.execute('SELECT item_id FROM cart WHERE user_id = ?', (user_id,))
    return cursor.fetchall()
