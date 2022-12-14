from typing import List
from fastapi import APIRouter, Depends, status
from pydantic.networks import EmailStr
from shopping_cart.controllers.address import (
    find_addresses_by_email,
    add_new_address,
    delete_address
)
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.schemas.address import AddressSchema
from shopping_cart.schemas.user import UserSchema

router = APIRouter(tags=['Address'], prefix='/address')


@router.post(
    '/', 
    summary="Add new address",
    description="Register new user address",
    status_code=status.HTTP_201_CREATED,
    response_model=AddressSchema
)
async def create_address_user(email: EmailStr, address: AddressSchema, current_user: UserSchema = Depends(get_current_user)):
    added_address = await add_new_address(email, address)
    return added_address


@router.get(
    '/', 
    summary="Get user addresses",
    description="Returns all registered user addresses",
    status_code=status.HTTP_200_OK,
    response_model=List[AddressSchema]
)
async def get_address(email: EmailStr, current_user: UserSchema = Depends(get_current_user)):
    user = await find_addresses_by_email(email)
    return user


@router.delete(
    '/', 
    summary="Delete user address",
    description="Remove one of the addresses registered by the user",
    status_code=status.HTTP_200_OK
)
async def delete_user_address(email: EmailStr, address: AddressSchema, current_user: UserSchema = Depends(get_current_user)):
    return await delete_address(email, address)