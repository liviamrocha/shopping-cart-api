from shopping_cart.schemas.address import Address
from shopping_cart.server.database import db
from shopping_cart.schemas.user import UserSchema, user_helper
from shopping_cart.schemas.address import address_helper



async def create_user(user: UserSchema):
    try:
        # Verifica se o usuário já existe
        user_email = await db.user_db.find_one({"email": user.email})
        if user_email:
            return {"message": "Usuário já registrado"}
        
        # Cria um novo usuário
        user_db = await db.user_db.insert_one(user.dict())
        
        if user_db.inserted_id:
            return {"message": "Usuário cadastrado"}
    except Exception as e:
            print(f'create_user.error: {e}')
    

async def get_user_by_email(email: str):
    try:
        user = await db.user_db.find_one({"email": email})
        if user:
            return user_helper(user)
    except Exception as e:
            print(f'get_user_by_email.error: {e}')
            

async def get_all_users():
    try: 
        users = []
        async for user in db.user_db.find():
                users.append(user_helper(user))
        return users
    except Exception as e:
            print(f'get_users.error: {e}')


async def update_password(email: str, new_password: str):
    try:
        user = await db.user_db.find_one_and_update(
            {"email": email},
            {"$set":
                {"password": new_password}})
        return {"message": "Senha atualizada"}
    except Exception as e:
        print(f"update_password_error: {e}")
    
    
async def create_address(user: UserSchema, address: Address):
    try:
        busca = await db.address_db.find_one({"user.email": user.email})
        if not busca:
            insert = await db.address_db.insert_one({
                "user": dict(user),
                "address": []
            })
        
        res = await db.address_db.find_one_and_update(
            {"user.email": user.email},
            {"$addToSet": {"address": dict(address)}}
        )
        return {"message": "Endereço cadastrado com sucesso"}
    except Exception as e:
        print(f"create_address_error: {e}")
        
        
async def find_address_by_email(email: str):
    try:
        user_email = await db.address_db.find_one({"user.email": email})
        return address_helper(user_email)
    except Exception as e:
        print(f'find_address_error: {e}')