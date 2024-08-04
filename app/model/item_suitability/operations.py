"""
item_id INTEGER
item_type TEXT
suitable_motherboard TEXT
suitable_cpu TEXT
suitable_gpu TEXT
suitable_ram TEXT
suitable_case TEXT
suitable_cooling TEXT
suitable_case TEXT
"""

"""
For all types use *

"""

ITEM_TYPES = ["cpu", "gpu", "psu", "motherboard", "ram", "case"]


from app.model.database_decorators import *

@get_from_database
def get_suitable_items(cursor, item_id, item_type) -> list:
    cursor.execute(f"SELECT suitable_{item_type} FROM item_suitability WHERE item_id = ?", (item_id,))
    items = cursor.fetchall()

    if len(items) == 0:
        raise UserWarning("Didn't find suitable item")

    items = items[0][0]

    if items == '*':
        return items

    return items.split(',')


@get_from_database
def get_item_type(cursor, item_id):
    cursor.execute(f"SELECT item_type FROM item_suitability WHERE item_id = ?", (item_id,))
    items = cursor.fetchall()

    if len(items) == 0:
        raise UserWarning("Didn't find suitable item")
    return items[0][0]

# @on_database_operation
# def change_item_

def append_item(item_id, item_id_to_append):
    item_to_append_type = get_item_type(item_id_to_append)

    list_of_current_suitable_items = get_suitable_items(item_id, item_to_append_type)

    if list_of_current_suitable_items == '*':
        return

    list_of_current_suitable_items.append(item_id_to_append)