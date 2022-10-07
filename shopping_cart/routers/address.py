from fastapi import APIRouter
from pydantic.networks import EmailStr
from shopping_cart.cruds.user import create_address, find_address_by_email
from shopping_cart.schemas.address import Address
from shopping_cart.schemas.user import UserSchema

router = APIRouter(tags=['Address'], prefix='/adresses')


# Criar um endereço
@router.post('')
async def create_address_user(user: UserSchema, address: Address):
    data = await create_address(user, address)
    return data

# Buscar um endereço pelo e-mail
@router.get('')
async def get_address(email: EmailStr):
    user = await find_address_by_email(email)
    return user