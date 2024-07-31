"""
item_id INTEGER PRIMARY KEY AUTOINCREMENT
item_name TEXT
description TEXT
sku TEXT
buy_price REAL
sell_price REAL
discount_price REAL
store_availability INTEGER
local_availability INTEGER
tags TEXT
photo (?) - Not implemented yet
"""

from app.model.database_decorators import *
from sqlite3 import OperationalError
import uuid


@get_from_database
def get_all_items_name_id(cursor):
    cursor.execute(f'SELECT item_id, item_name FROM items')
    return cursor.fetchall()


@get_from_database # TODO this func needs to be check what happiness on wrong id call, and return None
def get_item_by_id(cursor, item_id):
    cursor.execute(f'SELECT item_name, description, buy_price FROM items WHERE item_id = ?', (item_id,))
    item = cursor.fetchall()[0]
    print(f"get_item_by_id:{item}")
    return {'item_name': item[0], 'description': item[1], 'buy_price': item[2]}

@on_database_operation
def insert_into_items(cursor, item_name, description, sku, buy_price, sell_price,
                      discount_price, store_availability, local_availability, tags):
    if get_item_id_by_name(item_name):
        raise UserWarning("This item already exist in database")

    cursor.execute(f'INSERT INTO items (item_name, description, sku, buy_price, sell_price, '
                   f'discount_price, store_availability, local_availability, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (item_name, description, sku, buy_price, sell_price, discount_price, store_availability, local_availability, tags))


@get_from_database
def get_item_id_by_name(cursor, item_name):
    cursor.execute(f'SELECT item_id FROM items WHERE item_name = ?', (item_name,))
    item_id = cursor.fetchall()
    if len(item_id) == 0:
        return None
    return item_id[0][0]


def make_virtual_table_for_search(cursor, name):
    cursor.execute(f'CREATE VIRTUAL TABLE "{name}" USING FTS5(item_name, description, buy_price, store_availability, tags);')

def fill_virtual_table(cursor, name):
    cursor.execute(f'INSERT INTO "{name}" (item_name, description, buy_price, store_availability, tags) SELECT '
                   f'item_name, description, buy_price, store_availability, tags FROM items')

def remove_virtual_table(cursor, name):
    cursor.execute(f'DROP TABLE IF EXISTS "{name}"')


def search_item_by_name(cursor, search, name):
    # Zamiana name np. "karta graficzna" na "karta AND graficzna"
    search = ' AND '.join(search.lower().split(' '))
    cursor.execute(f'SELECT item_name, description, buy_price, store_availability FROM "{name}" WHERE tags MATCH ?', (search,))
    items = cursor.fetchall()
    return [{'item_name': row[0], 'description': row[1], 'buy_price': row[2], 'store_availability': row[3]} for row in items]


@on_database_operation
def search_in_database(cursor, search_phrase: str) -> list:
    table_name = str(uuid.uuid4()).encode('utf-8')

    # Try to create virtual table, if exist try different name
    while True:
        try:
            make_virtual_table_for_search(cursor, table_name)
            fill_virtual_table(cursor, table_name)
            break
        except OperationalError as e:
            print(f"Error {e}")
            table_name = str(uuid.uuid4()).encode('utf-8')

    print(f"Created table name: {table_name}")

    try:
        return search_item_by_name(cursor, search_phrase, table_name)
    except Exception as error:
        raise UserWarning(error)
    finally:
        remove_virtual_table(cursor, table_name)
