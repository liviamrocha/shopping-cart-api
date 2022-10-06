from shopping_cart.schemas.address import Address
from shopping_cart.server.database import db
from shopping_cart.schemas.user import UserSchema, user_helper
from shopping_cart.schemas.address import address_helper


# Criar um usuário
async def create_user(user: UserSchema):
    try:
        # Verifica se o usuário já existe
        user_email = await db.user_db.find_one({"email": user.email})
        if user_email:
            return {"message": "Usuário já registrado"}
        
        # Cria um novo usuário
        user_db = await db.user_db.insert_one(user.dict())
        
        # Valida o cadastro e retorna a mensagem
        if user_db.inserted_id:
            return {"message": "Usuário cadastrado"}
        
    # Retona a mensagem de erro
    except Exception as e:
            print(f'create_user.error: {e}')
    

# Buscar um usuário pelo e-mail
async def get_user_by_email(email: str):
    try:
        # Busca o e-mail no banco de dados e retorna no modelo do "helper"
        user = await db.user_db.find_one({"email": email})
        if user:
            return user_helper(user)
        
    # Retona a mensagem de erro
    except Exception as e:
            print(f'get_user_by_email.error: {e}')
            

# Buscar todos os usuários
async def get_all_users():
    try: 
        # Cria uma lista vazia, faz uma busca no banco de dados, acrescenta o usuário à lista e retorna a lista
        users = []
        async for user in db.user_db.find():
                users.append(user_helper(user))
        return users
    
    # Retona a mensagem de erro
    except Exception as e:
            print(f'get_users.error: {e}')


# Atualizar a senha
async def update_password(email: str, new_password: str):
    try:
        # Busca o usuário no banco de dados, atualiza a senha e retorna a mensagem
        update = await db.user_db.find_one_and_update(
            {"email": email},
            {"$set":
                {"password": new_password}})
        if update:
            return {"message": "Senha atualizada"}
        return {"message": "Usuário não encontrado"}
    
    # Retona a mensagem de erro
    except Exception as e:
        print(f"update_password_error: {e}")
    

# Criar um endereço
async def create_address(user: UserSchema, address: Address):
    try:
        # Busca se um usuário já existe no banco de dados
        busca = await db.address_db.find_one({"user.email": user.email})
        # Caso o usuário não exista, cria o usuário e uma lista vazia de endereço
        if not busca:
            await db.address_db.insert_one({
                "user": dict(user),
                "address": []
            })
        # Busca o usuário, adiciona o endereço e retorna a mensagem
        await db.address_db.find_one_and_update(
            {"user.email": user.email},
            {"$addToSet": {"address": dict(address)}}
        )
        return {"message": "Endereço cadastrado com sucesso"}
    
    # Retona a mensagem de erro
    except Exception as e:
        print(f"create_address_error: {e}")
        

# Buscar endereço pelo e-mail
async def find_address_by_email(email: str):
    try:
        # Busca um usuário pelo e-mail e retorna no modelo do "helper"
        user_email = await db.address_db.find_one({"user.email": email})
        if user_email:
            return address_helper(user_email)
        return {"message": "Usuário não possui endereço cadastrado"}
    
    # Retona a mensagem de erro
    except Exception as e:
        print(f'find_address_error: {e}')