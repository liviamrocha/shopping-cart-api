from typing import List, Optional
from fastapi import HTTPException, status
from pydantic.networks import EmailStr
import shopping_cart.cruds.user as user_crud
from shopping_cart.cruds.cart import delete_cart, get_user_cart
from shopping_cart.schemas.user import (
    PasswordUpdateSchema,
    UserResponse,
    UserSchema
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
)
from shopping_cart.core.security import get_password, verify_password

from shopping_cart.server.database import db

class UserService:
    @staticmethod
    async def create_user_security(user: UserSchema):
        user_in = UserSchema(
            name=user.name,
            email=user.email,
            password=get_password(user.password)
        )
        await validate_user(user)
        if user:
            await db.user_db.insert_one(user_in.dict())
            return user_in
        
    @staticmethod
    async def authenticate(email: str, password: str):
        user = await search_user_by_email(email)
        if user:
            if not verify_password(password=password, hashed_password=user["password"]):
                return None
            return user
        
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[UserSchema]:
        user = await db.user_db.find_one({"email": email})
        return user        


async def validate_user(user: UserSchema, input_code: Optional[str] = None):

    is_new_user = input_code is None

    input_user = await user_crud.get_user_by_email(user.email)

    if input_user is not None and is_new_user:
        raise AlreadyExistException("Cannot create user. A user with the same e-mail already exists")


async def create_new_user(user: UserSchema) -> UserResponse:

    await validate_user(user)

    new_user = user.dict()
    await user_crud.create_user(new_user)
    created_user = UserResponse(**new_user)
    return created_user

    
async def get_all_users() -> List[dict]:
    users = await user_crud.get_all_users()
    return users


async def search_user_by_email(
    email: EmailStr, 
    raise_exception: bool = True
) -> Optional[dict]:

    user = await user_crud.get_user_by_email(email)

    if not user and raise_exception:
        raise NotFoundException('User not found')
    return user


async def update_user_password(email: EmailStr, password_data: PasswordUpdateSchema):

    user = await search_user_by_email(email)
    
    if verify_password(password_data.current_password, user["password"]):
    
        new_pass = get_password(password_data.new_password)

        await user_crud.update_password(
            email, new_pass
        )
        updated_user = await search_user_by_email(email)
        return updated_user
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password")

async def delete_user(email: EmailStr):

    await search_user_by_email(email)

    cart = await get_user_cart(email)
    if cart:
        await delete_cart(email)

    await user_crud.delete_user(email)
    return {"message": "User has been successfully deleted"}




