from typing import List, Optional
from pydantic.networks import EmailStr
import shopping_cart.cruds.address as address_crud
from shopping_cart.controllers.user import search_user_by_email
from shopping_cart.schemas.address import (
    AddressSchema, 
    AddressResponseSchema
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
    DataConflictException
)

async def validate_address(email: EmailStr, address: AddressSchema, raise_exception=False):

    await search_user_by_email(email)

    user_exist = await address_crud.find_user(email)
    if not user_exist:
        raise NotFoundException('User has no registered addresses')

    input_address = await address_crud.find_address(email, address.dict())
    if input_address is not None and raise_exception:
        raise AlreadyExistException("Address already exists for this user")

    return input_address

async def add_new_address(email: EmailStr, address=AddressSchema):

    user = await search_user_by_email(email)
    input_address = await address_crud.find_address(email, address.dict())
    if input_address is not None:
        raise AlreadyExistException("Address already exists for this user")

    check_address = await address_crud.find_user(email)
    if check_address is None:
        await address_crud.create_address(user)

    if address.is_delivery:
        await address_crud.update_delivered_address(email)

    new_address = address.dict()
    await address_crud.add_address(email, new_address)
    added_address = AddressSchema(**new_address)

    return added_address


async def find_addresses_by_email(
    email: EmailStr, 
    raise_exception: bool = True
) -> Optional[dict]:

    await search_user_by_email(email)

    address = await address_crud.find_addresses_by_email(email)
    if not address and raise_exception:
        raise NotFoundException('User has no registered addresses')
    return address['address']

async def find_delivery_address(email: EmailStr):

    await search_user_by_email(email)
    await find_addresses_by_email(email)

    delivery_address = await address_crud.get_delivery_address(email)
    if not delivery_address:
        raise NotFoundException('User has no registered addresses')
    return delivery_address


async def delete_address(email: EmailStr, address: AddressSchema):

    await validate_address(email, address)

    removed = await address_crud.delete_address(email, address.dict())
    if not removed:
        raise NotFoundException('Address provided is not registered for this user')

    if address.is_delivery:
        await address_crud.update_delivered_automatically(email)

    return {"message": "Address successfully deleted"}

