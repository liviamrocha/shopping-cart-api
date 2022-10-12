from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, List
import jwt
from pydantic import ValidationError
from pydantic.networks import EmailStr
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.core.security import create_access_token, create_refresh_token
from shopping_cart.core.security import create_access_token, create_refresh_token, settings_auth
from shopping_cart.schemas.auth_schema import TokenPayload, TokenSchema
from shopping_cart.schemas.user import (
    PasswordUpdateSchema, 
    UserSchema,
    UserResponse,
    AuthenticationResponseSchema
)
from shopping_cart.controllers.user import (
    UserService,
    get_all_users,
    search_user_by_email,
    update_user_password,
    delete_user
)
from shopping_cart.controllers.user import UserService



router = APIRouter(tags=['User'], prefix='/user')


@router.post(
    '/', 
    summary="Create user",
    description="Registration of a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=AuthenticationResponseSchema
)
async def post_user(user: UserSchema):
    new_user = await UserService.create_user_security(user)
    return new_user


@router.get(
    '/',
    summary="Get all registered users.",
    description="Search for all registered users.",
    response_model=List[UserResponse]
)
async def get_users(current_user: UserSchema = Depends(get_current_user)):
    users_list = await get_all_users()
    return users_list
    

@router.get(
    '/email', 
    summary="Get user by e-mail",
    description="Search for a user by e-mail",
    response_model=UserResponse
)
async def get_user_by_email(email: EmailStr, current_user: UserSchema = Depends(get_current_user)):
    user = await search_user_by_email(email)
    return user
    

@router.put(
    "/password",
    summary="Update password",
    description="Update user password",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AuthenticationResponseSchema 
) 
async def password_update(email: EmailStr, password_data: PasswordUpdateSchema, current_user: UserSchema = Depends(get_current_user)):
    updated_user =  await update_user_password(email, password_data)
    return updated_user


@router.delete(
    '/', 
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete user",
    description="Delete user by e-mail",
)
async def delete_user_by_email(email: EmailStr, current_user: UserSchema = Depends(get_current_user)):
    user = await delete_user(email)
    return user