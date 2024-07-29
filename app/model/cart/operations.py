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
def add_to_cart_database(cursor, item_id, amount, user_hash):
    cursor.execute('INSERT INTO cart (session_hash, item_id, amount) VALUES (?, ?, ?)', (user_hash, item_id, amount))


@on_database_operation
def update_amount(cursor, item_id, new_amount, user_hash):
    cursor.execute('UPDATE cart SET amount = ? WHERE session_hash = ? AND item_id = ?', (new_amount, user_hash, item_id))


@get_from_database
def get_current_item_amount_in_cart(cursor, user_hash, item_id):
    cursor.execute('SELECT amount FROM cart WHERE session_hash = ? AND item_id = ?', (user_hash, item_id))
    # output should look like that [(1,)] - so [0] to get tuple and [0] to get value
    # also if there is a couple of same item entries func will return only amount of first in database
    # rest should be considered as error
    output = cursor.fetchall()

    # if item is not in database, current amount is 0
    if len(output) == 0:
        return 0

    if len(output) > 1:
        raise UserWarning('More then one same item entry in database')

    return output[0][0]


@on_database_operation
def remove_from_cart_database(cursor, user_hash, item_id):
    cursor.execute('DELETE FROM cart WHERE session_hash = ? AND item_id = ?', (user_hash, item_id))