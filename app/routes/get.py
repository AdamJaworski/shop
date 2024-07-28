from app.auth.auth import get_new_session_hash, is_hash_in_database
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from config import HTML_DIR


router = APIRouter()


@router.get("/")
async def root(request: Request):
    with open(HTML_DIR + "/index.html") as f:
        response = HTMLResponse(content=f.read(), status_code=200)

    cookie_value = request.cookies.get('cart_cookie')

    # if cookie is not in database or doesn't exist we need to set it
    if not cookie_value or not is_hash_in_database(cookie_value):
        response.set_cookie(key='cart_cookie', value=get_new_session_hash())

    return response


