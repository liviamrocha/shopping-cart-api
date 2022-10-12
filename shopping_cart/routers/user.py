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
    UserResponse
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
    

@router.post('/test-token', 
             summary="Test if the access token is valid", 
             response_model=UserSchema
)
async def test_token(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@router.post('/refresh',
             summary="Refresh token",
             response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings_auth.JWT_REFRESH_SECRET_KEY, algorithms=[settings_auth.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    user = await UserService.get_user_by_email(token_data.sub)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return{
    "access_token": create_access_token(user["email"]),
    "refresh_token": create_refresh_token(user["email"])
}
        


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
    response_model=UserResponse 
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
async def delete_user_by_email(email: EmailStr):
    user = await delete_user(email)
    return user