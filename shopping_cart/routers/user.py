from fastapi import APIRouter
from pydantic import EmailStr
from shopping_cart.schemas.address import Address
from shopping_cart.schemas.user import UserSchema
from shopping_cart.cruds.user import create_address, create_user, get_all_users, get_user_by_email, update_password, find_address_by_email

router = APIRouter(tags=['User'], prefix='/user')

# Criar um usuário
@router.post('')
async def post_user(user: UserSchema):
    message = await create_user(user)
    return message

# Buscar um usuário pelo e-mail
@router.get('/email/')
async def get_user_email(email: str):
    user = await get_user_by_email(email)
    return user

# Buscar todos os usuários
@router.get('/all/')
async def get_all():
    users_list = await get_all_users()
    return users_list

# Atualizar a senha
@router.put("/update")
async def password_update(email: EmailStr, new_password: str):
    update = await update_password(email, new_password)
    return update