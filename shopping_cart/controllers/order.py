import uuid
from typing import List, Optional
from pydantic import EmailStr
import shopping_cart.cruds.order as order_crud
from bson.binary import UuidRepresentation
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.order import OrderResponseSchema
from shopping_cart.controllers.exceptions.custom_exceptions import NotFoundException
from shopping_cart.controllers.cart import has_cart, clean_user_cart
from shopping_cart.controllers.product import update_product_inventory
from shopping_cart.controllers.user import search_user_by_email
from shopping_cart.controllers.address import find_delivery_address



async def validate_cart(email: EmailStr):
    if not await has_cart(email):
        raise NotFoundException("User's shopping cart is empty")

async def create_order(email: EmailStr):
    await search_user_by_email(email)
    await validate_cart(email)

    order_id = str(uuid.uuid1())
    delivery_address = await find_delivery_address(email)

    await update_payment_status(email)
    await order_crud.create_order(email, delivery_address, order_id)
    await clean_user_cart(email)
    await update_product_stock(order_id)


    return {"order_id": order_id}

async def find_user_orders(email: EmailStr) -> List[OrderResponseSchema]:
    await search_user_by_email(email)
    await find_user(email)

    orders = await order_crud.get_orders(email)
    return orders

async def find_order_by_id(
    order_id: str,
    raise_exception: bool = True
) -> Optional[dict]:

    order = await order_crud.get_order_by_id(order_id)

    if not order and raise_exception:
        raise NotFoundException('Order not found')
    return order

async def find_order_items(email: EmailStr, order_id: str):
    await search_user_by_email(email)
    await find_user(email)
    await check_order_id_by_user(email, order_id)

    items = await order_crud.get_itens_from_order(email, order_id)
    return items

async def find_total_orders(email: EmailStr):
    await search_user_by_email(email)
    await find_user(email)

    total_orders = await order_crud.get_orders_count(email)
    return {"total_orders": total_orders}

# Funções auxiliares
async def update_payment_status(email: EmailStr):
    return await order_crud.update_payment_status(email)

async def update_product_stock(order_id):
    order = await find_order_by_id(order_id)
    await update_product_inventory(order)

async def find_user(email: EmailStr):
    find_user_order = await order_crud.find_user_order(email)
    if not find_user_order:
        raise NotFoundException("User has no registered orders")
    return find_user_order

async def check_order_id_by_user(email: EmailStr, order_id: str):
    await search_user_by_email(email)
    await find_user(email)

    find_user_order = await order_crud.validade_order_for_user(email, order_id)
    if not find_user_order:
        raise NotFoundException("Order not found for the informed user")
    return find_user_order


  



