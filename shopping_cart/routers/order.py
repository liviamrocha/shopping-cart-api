from typing import List
from fastapi import APIRouter, status
from pydantic import EmailStr
from shopping_cart.schemas.order import OrderResponseSchema
from shopping_cart.schemas.order_items import OrderItemSchema
from shopping_cart.controllers.order import (
    create_order,
    find_user_orders,
    find_order_by_id,
    find_order_items,
    find_total_orders
)

router = APIRouter(tags=['Orders'], prefix='/orders')

@router.post(
    '/', 
    summary="Close order",
    description="Close the user's shopping cart and create an order",
    status_code=status.HTTP_201_CREATED,
)
async def add_order(email: EmailStr):
    order_id = await create_order(email)
    return order_id

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[OrderResponseSchema],
    summary="Get closed orders",
    description="Search for all closed user orders",
)
async def get_orders(email: EmailStr):
    orders = await find_user_orders(email)
    return orders

@router.get(
    '/id',
    status_code=status.HTTP_200_OK,
    response_model=OrderResponseSchema,
    summary="Get closed order by id.",
    description="Search for a closed order by id",
)
async def get_order(order_id: str):
    order = await find_order_by_id(order_id)
    return order

@router.get(
    '/items',
    status_code=status.HTTP_200_OK,
    response_model=List[OrderItemSchema],
    summary="Get closed order by id.",
    description="Search for a closed order by id"
)
async def get_items(email: EmailStr, order_id: str):
    items = await find_order_items(email, order_id)
    return items

@router.get(
    '/count',
    status_code=status.HTTP_200_OK,
    summary="Get total orders",
    description="Return total of user orders",
)
async def orders_count(email: EmailStr):
    total_orders = await find_total_orders(email)
    return total_orders

