import time
from datetime import timedelta
from app.utilities.auth import get_new_session_hash, is_hash_in_database, set_last_visit
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from config import HTML_DIR


router = APIRouter()



@router.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    with open(HTML_DIR + "/index.html", encoding='utf-8') as f:
        response = HTMLResponse(content=f.read(), status_code=200)

    cookie_value = request.cookies.get('cart_cookie')

    # if cookie is not in database or doesn't exist we need to set it
    if not cookie_value or not is_hash_in_database(cookie_value):
        # TODO trzeba się dogadać czy potrzebny jest tutaj expire
        response.set_cookie(key='cart_cookie', value=get_new_session_hash(), expires=int(timedelta(days=30).total_seconds()))

    else:
        set_last_visit(cookie_value, time.time())

    return response


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    with open(HTML_DIR + "/search.html", encoding='utf-8') as f:
        response = HTMLResponse(content=f.read(), status_code=200)

    return response


if __name__ == "__main__":
    pass
