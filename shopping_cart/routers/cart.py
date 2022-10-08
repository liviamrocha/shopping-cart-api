
from fastapi import APIRouter
from pydantic import EmailStr
from shopping_cart.cruds.cart import add_product_cart, create_cart, find_cart_by_email

from shopping_cart.schemas.cart import CartSchema
from shopping_cart.schemas.order_item import OrderItemSchema
from shopping_cart.schemas.user import UserSchema

router = APIRouter(tags=['Carts'], prefix='/carts')

@router.post('')
async def add_cart(cart: CartSchema):
    message = await create_cart(cart)
    return message

@router.post('/item')
async def add_item(email: EmailStr, code: int, quantity: int):
    message = await add_product_cart(email, code, quantity)
    return message

@router.get('')
async def get_cart_by_email(email: EmailStr):
    message = await find_cart_by_email(email)
    return message