import sqlite3
import os
from pathlib import Path
from config import DATABASE_PATH, DATABASE_FOLDER_PATH


def init_database() -> None:
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.cursor()

    create_users_table = '''
    CREATE TABLE IF NOT EXISTS user_task (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
    );
    '''

    create_items_table = '''
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        description TEXT,
        sku TEXT,
        buy_price REAL,
        sell_price REAL,
        discount_price REAL,
        store_availability INTEGER,
        local_availability INTEGER
    );
    '''

    create_cart_table = '''
    CREATE TABLE IF NOT EXISTS cart (
        user_id INTEGER,
        item_id INTEGER,
        amount INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (item_id) REFERENCES items(item_id)
    ); 
    '''

    cursor.execute(create_users_table)
    cursor.execute(create_items_table)
    cursor.execute(create_cart_table)

    db.commit()
    db.close()


if __name__ == "__main__":
    Path(DATABASE_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
    try:
        os.remove(DATABASE_PATH)
    except Exception:
        pass
    init_database()
