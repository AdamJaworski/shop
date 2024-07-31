from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.model.cart.operations import *
from app.model.items.operations import insert_into_items, search_in_database, get_item_id_by_name
router = APIRouter()


@router.post("/get_cart")
async def get_cart(request: Request):
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    user_cart = get_user_cart(cookie_value)

    user_cart = [
        {
            'item_id': item,
            'amount': amount
        } for item, amount in user_cart
    ]

    return JSONResponse(content={"user_cart": user_cart}, status_code=200)


@router.post("/add_to_cart")
async def add_to_cart(request: Request, item_id: str, amount: int):
    """
    Adds item by id to user cart. If user wants to increase amount of items in his cart, this should be called with
    amount user wants to add
    """
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    if not item_id or not amount:
        raise HTTPException(status_code=400, detail="No item or amount found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Wrong amount - did you mean to use /remove_from_cart?")

    try:
        # if item is already in user cart , we need to increase its number
        current_amount = get_current_item_amount_in_cart(cookie_value, item_id)

        if current_amount > 0:
            amount += current_amount
            update_amount(item_id, amount, cookie_value)
        else:
            add_to_cart_database(item_id, amount, cookie_value)

        return JSONResponse(content={'status': True}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")


@router.post("/remove_from_cart")
async def add_to_cart(request: Request, item_id: str, amount: int):
    """
    Removes item by id from user cart. If user wants to decrease amount of items in his cart, this should be called with
    amount user wants to remove. If amount of items will be <= 0, then item will be removed
    """
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    if not item_id or not amount:
        raise HTTPException(status_code=400, detail="No item or amount found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Wrong amount - did you mean to use /add_to_cart?")

    try:
        current_amount = get_current_item_amount_in_cart(cookie_value, item_id)

        if (current_amount - amount) <= 0:
            remove_from_cart_database(cookie_value, item_id)
        else:
            update_amount(item_id, current_amount - amount, cookie_value)

        return JSONResponse(content={'status': True}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")


@router.post("/search")
async def search(request: Request, query: str):
    try:
        return JSONResponse(content=search_in_database(query), status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")


@router.post("/debug/add_item")
async def add_item(request: Request, item_name: str, description: str, sku: str, buy_price: float, sell_price: float,
                   discount_price: float, store_availability: int, local_availability: int, tags: str):
    try:
        insert_into_items(item_name, description, sku, buy_price, sell_price,
                          discount_price, store_availability, local_availability, tags.lower())

        item_id = get_item_id_by_name(item_name)
        return JSONResponse(content={'item_id': item_id}, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")

