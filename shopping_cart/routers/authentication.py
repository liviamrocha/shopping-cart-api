import jwt
from typing import Any, List
from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.core.security import create_access_token, create_refresh_token
from shopping_cart.core.security import create_access_token, create_refresh_token, settings_auth
from shopping_cart.schemas.auth_schema import TokenPayload, TokenSchema
from shopping_cart.schemas.user import UserSchema, AuthenticationResponseSchema


from shopping_cart.controllers.user import UserService

router = APIRouter(tags=['Authentication'], prefix='/auth')

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
    

@router.post(
    '/test-token', 
    summary="Test if the access token is valid", 
    response_model=AuthenticationResponseSchema
)
async def test_token(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@router.post(
    '/refresh-token',
    summary="Refresh token",
    response_model=TokenSchema
)
async def refresh_token(refresh_token: str = Body(...), current_user: UserSchema = Depends(get_current_user)):
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