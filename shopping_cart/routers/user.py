from fastapi import APIRouter, status, Body
from typing import List
from pydantic.networks import EmailStr
from shopping_cart.schemas.user import (
    PasswordUpdateSchema, 
    UserSchema,
    UserResponse
)
from shopping_cart.controllers.user import (
    UserService,
    create_new_user,
    get_all_users,
    search_user_by_email,
    update_user_password,
)
from shopping_cart.auth.auth_handler import signJWT


router = APIRouter(tags=['User'], prefix='/user')



@router.post(
    '/login'
)







@router.post(
    '/', 
    summary="Create user",
    description="Registration of a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchema
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
async def get_users():
    users_list = await get_all_users()
    return users_list
    

@router.get(
    '/email', 
    summary="Get user by e-mail",
    description="Search for a user by e-mail",
    response_model=UserResponse
)
async def get_user_by_email(email: EmailStr):
    user = await search_user_by_email(email)
    return user
    

@router.put(
    "/password",
    summary="Update password",
    description="Update user password",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UserResponse 
) 
async def password_update(email: EmailStr, password_data: PasswordUpdateSchema):
    updated_user =  await update_user_password(email, password_data)
    return updated_user