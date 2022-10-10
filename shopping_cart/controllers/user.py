from typing import List, Optional
from pydantic.networks import EmailStr
import shopping_cart.cruds.user as user_crud
from shopping_cart.schemas.user import (
    UserSchema, 
    PasswordUpdateSchema, 
    UserResponse
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
)


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

    await search_user_by_email(email)

    password_to_update = password_data.dict()
    await user_crud.update_password(
        email, password_to_update
    )
    updated_user = await search_user_by_email(email)
    return updated_user


