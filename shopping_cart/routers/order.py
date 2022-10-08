from fastapi import APIRouter
from shopping_cart.cruds.order import create_order

from shopping_cart.schemas.user import UserSchema

router = APIRouter(tags=['Orders'], prefix='/orders')


@router.post('')
async def add_order(user: UserSchema):
    message = await create_order(user)
    return message