
from fastapi import APIRouter, status
from pydantic import EmailStr
from shopping_cart.controllers.cart import (
    fetch_cart_by_email, 
    add_cart_item,
    remove_cart_item, 
    clean_user_cart
)
from shopping_cart.schemas.cart import CartRequestSchema, CartResponseSchema


router = APIRouter(tags=['Carts'], prefix='/carts')


@router.post(
    '/', 
    summary="Add item to a cart",
    description="Add new item to user's shopping cart",
    status_code=status.HTTP_201_CREATED,
)
async def add_item(email: EmailStr, cart_item: CartRequestSchema):
    return await add_cart_item(email, cart_item)

@router.get(
    '/', 
    response_model=CartResponseSchema,
    summary="Get shopping cart",
    description="Returns user's shopping cart",
)
async def get_cart_by_email(email: EmailStr):
    cart = await fetch_cart_by_email (email)
    return cart

@router.delete(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete item",
    description="Remove item from user's shopping cart",
)
async def remove_item(email: EmailStr, cart_data: CartRequestSchema):
    return await remove_cart_item(email, cart_data)

@router.delete(
    "/all",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Clean cart",
    description="Removes all items from the shopping cart",
)
async def clean_cart(email: EmailStr):
    return await clean_user_cart(email)