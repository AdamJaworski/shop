from fastapi import APIRouter, Request, Response
from app.model.items.operations import get_all_items_name_id, get_item_by_id
from fastapi.responses import HTMLResponse
from config import *
import os

router = APIRouter()


def init_item_routes():
    for item in get_all_items_name_id():
        name = '-'.join(item[1].split(' '))
        item_id = str(item[0])
        router.add_api_route(f"/{name}-{item_id}", create_route_for_item(item_id), methods=["GET"])

def create_route_for_item(item_id):
    async def item_page(request: Request):
        file_path = os.path.join(HTML_DIR, f"{item_id}.html")
        if not os.path.isfile(file_path):
            return HTMLResponse(content="Item not found", status_code=404)
        with open(file_path, "r", encoding='utf-8') as f:
            response = HTMLResponse(content=f.read(), status_code=200)
        return response

    return item_page


#  requires dynamic root deploy to work
# def add_item_route_function(item_id):
#     item = get_item_by_id(item_id)
#     name = '-'.join(item['item_name'].split(' '))
#     router.add_api_route(f"/{name}-{item_id}", create_route_for_item(item_id), methods=["GET"])


# Not working
# @router.post("/debug/add_item_route")
# async def add_item_route(request: Request, item_id: int):
#     try:
#         add_item_route_function(item_id)
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")
#
#     return JSONResponse(content={'status': True}, status_code=200)