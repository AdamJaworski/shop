from fastapi import APIRouter, Request, Response, HTTPException
from app.model.cart.operations import *

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

    return {"user_cart": user_cart}


@router.post("/add_to_cart")
async def add_to_cart(request: Request, item_id: str, amount: int):
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

        return {'status': True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")


@router.post("/remove_from_cart")
async def add_to_cart(request: Request, item_id: str, amount: int):
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

        return {'status': True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error: {e}, occurred")