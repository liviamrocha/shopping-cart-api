from fastapi import APIRouter
from pydantic import EmailStr
from shopping_cart.cruds.order import count_orders, create_order, find_orders, find_product_quantity

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('')
async def add_order(email: EmailStr):
    message = await create_order(email)
    return message

@router.get('/email')
async def get_orders(email: EmailStr):
    message = await find_orders(email)
    return message

@router.get('/email/products')
async def get_products(email: EmailStr):
    message = find_product_quantity(email)
    return message

@router.get('/count')
async def orders_count(email: EmailStr):
    message = count_orders(email)
    return message

