from typing import List, Optional
from pydantic.networks import EmailStr
import shopping_cart.cruds.address as address_crud
from shopping_cart.controllers.user import search_user_by_email
from shopping_cart.schemas.address import (
    AddressSchema, 
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
    DataConflictException
)


async def add_new_address(email: EmailStr, address=AddressSchema):

    # Checa se usuário existe para o email informado. Caso não exista, levanta exceção.
    user = await search_user_by_email(email)

    # Checa se o usuário possui endereços cadastrados
    # Se não existir, cria um documento com array de endereços vazio
    check_address = await address_crud.find_user(email)
    if check_address is None:
        await address_crud.create_address(user)

    # Se o novo endereço for is_delivery=True, seta os que estão no banco como True para False
    if address.is_delivery:
        await address_crud.update_delivered_address(email)

    # Adiciona o endereço à lista de endereços
    new_address = address.dict()
    await address_crud.add_address(email, new_address)
    added_address = AddressSchema(**new_address)

    return added_address


async def find_addresses_by_email(
    email: EmailStr, 
    raise_exception: bool = False
) -> Optional[dict]:

    await search_user_by_email(email)

    address = await address_crud.find_address_by_email(email)
    if not address:
        raise NotFoundException('User has no registered address')

    return address['address']

