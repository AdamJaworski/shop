"""
session_hash TEXT PRIMARY KEY,
create_time REAL,
last_visit REAL
"""

from app.model.database_decorators import *


@get_from_database
def is_hash_in_database(cursor, _hash: str):
    cursor.execute('SELECT * FROM session WHERE session_hash = ?', (_hash,))
    hash_id = cursor.fetchall()
    return False if len(hash_id) == 0 else True


@on_database_operation
def add_hash_to_database(cursor, session_hash: str, create_time: float, last_visit: float):
    cursor.execute('INSERT INTO session (session_hash, create_time, last_visit) VALUES (?, ?, ?)', (session_hash, create_time, last_visit))


@on_database_operation
def set_last_visit(cursor, session_hash: str, last_visit: float):
    cursor.execute('UPDATE session SET last_visit = ? WHERE session_hash = ?', (last_visit, session_hash))