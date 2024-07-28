from fastapi import APIRouter, Request, Response, HTTPException
from app.model.cart.operations import get_user_cart, add_to_cart_database

router = APIRouter()


@router.post("/get_cart")
async def get_cart(request: Request):
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    # TODO to trzeba wytestować - jak wyglądają zwracane dane, jak je sformatować
    user_cart = get_user_cart(cookie_value)

    return {"user_cart": user_cart}


@router.post("/add_to_cart")
async def add_to_cart(request: Request):
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    try:
        item = request.get('item_id')
        amount = request.get('amount')

        if not item or not amount:
            raise HTTPException(status_code=400, detail="No item or amount found")

        add_to_cart_database(item, amount, cookie_value)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error {e} occurred")

    return {'status': True}


