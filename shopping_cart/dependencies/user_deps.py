from datetime import datetime
from pydantic import ValidationError
from fastapi import HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from shopping_cart.controllers.user import UserService
from shopping_cart.schemas.auth_schema import TokenPayload


from shopping_cart.schemas.user import UserSchema
from shopping_cart.auth.auth_handler import settings
from shopping_cart.cruds.user import get_user_by_email


reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reusable_oauth)) -> UserSchema:
    try:
        payload = jwt.encode(
            token, settings.JWT_SECRET_KEY, algorithm=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except(jwt.JWTError, ValidationError):
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
    
    return user