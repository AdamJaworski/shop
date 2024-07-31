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
photo (?) - Not implemented yet
"""

from app.model.database_decorators import *


@on_database_operation
def insert_into_items(cursor, item_name, description, sku, buy_price, sell_price,
                      discount_price, store_availability, local_availability):

    cursor.execute(f'INSERT INTO items (item_name, description, sku, buy_price, sell_price, '
                   f'discount_price, store_availability, local_availability) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (item_name, description, sku, buy_price, sell_price, discount_price, store_availability, local_availability))


@on_database_operation
def make_virtual_table_for_search(cursor):
    cursor.execute('CREATE VIRTUAL TABLE items_fts USING FTS5(item_name, description, buy_price, store_availability);')


@on_database_operation
def fill_virtual_table(cursor):
    cursor.execute('INSERT INTO items_fts(item_name, description, buy_price, store_availability) SELECT item_name,'
                   ' description, buy_price, store_availability FROM items')


@on_database_operation
def remove_virtual_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS items_fts')


@get_from_database
def search_item_by_name(cursor, search: str):
    make_virtual_table_for_search()
    fill_virtual_table()

    # Zamiana name np. "karta graficzna" na "karta AND graficzna"
    search = ' AND '.join(search.lower().split(' '))
    cursor.execute('SELECT item_name, description, buy_price, store_availability FROM items_fts WHERE items_fts MATCH ?', (search,))
    items = cursor.fetchall()
    items = [{'item_name': row[0], 'description': row[1], 'buy_price': row[2], 'store_availability': row[3]} for row in items]

    remove_virtual_table()
    return items
