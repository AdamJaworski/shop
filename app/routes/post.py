from fastapi import APIRouter, Request, Response, HTTPException
from app.model.cart.operations import get_user_cart

router = APIRouter()


@router.post("/get_cart")
async def get_cart(request: Request):
    cookie_value = request.cookies.get('cart_cookie')

    if not cookie_value:
        raise HTTPException(status_code=400, detail="Cart cookie not found")

    # TODO to trzeba wytestować - jak wyglądają zwracane dane, jak je sformatować
    user_cart = get_user_cart(cookie_value)

    return {"user_cart": user_cart}
