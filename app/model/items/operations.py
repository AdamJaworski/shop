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
photo (?)
"""

from app.model.database_decorators import *