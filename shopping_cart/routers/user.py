from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, List
from pydantic.networks import EmailStr
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.core.security import create_access_token, create_refresh_token
from shopping_cart.schemas.auth_schema import TokenSchema
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
from shopping_cart.controllers.user import UserService


router = APIRouter(tags=['User'], prefix='/user')



@router.post(
    '/login',
    summary="User login",
    description="Create access and refresh tokens for user",
    response_model=TokenSchema
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    return{
        "access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user["email"])
    }
    
@router.post('test-token', 
             summary="Test if the access token is valid", 
             response_model=UserSchema
)
async def test_token(user: UserSchema = Depends(get_current_user)):
    return user






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