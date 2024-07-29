import time, hashlib
from app.model.session.operations import *


def generate_hash() -> str:
    x = int(time.time() * 10e7)
    x ^= x << 22
    x ^= x >> 26
    x ^= x << 4
    x ^= int(time.time() * 10e7)
    x = hashlib.sha256(str(x).encode('utf-8'))
    return x.hexdigest()


def generate_new_session_hash() -> str:
    _hash = generate_hash()
    return _hash if not is_hash_in_database(_hash) else generate_new_session_hash()


def get_new_session_hash() -> str:
    _hash = generate_new_session_hash()
    add_hash_to_database(_hash, time.time(), time.time())
    return _hash

