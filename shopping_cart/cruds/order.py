from pydantic import EmailStr
from shopping_cart.schemas.order import order_helper
from shopping_cart.server.database import db




# Transforma um carrinho em um pedido
async def create_order(email: EmailStr):
    try:
        # Busca o carrinho no database
        find_cart = await db.cart_db.find_one({"user.email": email})
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        
        # Valida se o usuário tem um endereço de entrega cadastrado
        address = await db.address_db.find_one({"user.email": email, "address.is_delivery": True})
        if not address:
            return {"message": "Usuário não possui endereço de entrega cadastrado"}
        
        
        
        
        agora_vai = db.cart_db.aggregate([
            {"$match": { "user.email": email}},
            {"$addFields": {"address": dict(address)}},
            {"$merge": {"into": "order"}}
        ])
        agora_vai_lista = await agora_vai.to_list(length=100)
        print(agora_vai)
        print(agora_vai_lista)
            
        return {"message": "vixi maria"}
            
        # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')