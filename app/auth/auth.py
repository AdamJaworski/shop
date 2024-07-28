from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import time, hashlib
from app.model.session.operations import is_hash_in_database, add_hash_to_database
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     if token != "fake-super-secret-token":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return {"username": "testuser"}


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
    add_hash_to_database(_hash, time.time())
    return _hash
