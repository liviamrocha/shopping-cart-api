from fastapi import APIRouter
from pydantic import EmailStr
from shopping_cart.cruds.order import create_order

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('')
async def add_order(email: EmailStr):
    message = await create_order(email)
    return message