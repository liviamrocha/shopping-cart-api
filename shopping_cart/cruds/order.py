from pydantic import EmailStr
from shopping_cart.server.database import db




# Transforma um carrinho em um pedido
async def create_order(email: EmailStr):
    try:
        # Busca o carrinho no database
        find_cart = await db.cart_db.find_one({"user.email": email})
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        address = await db.address_db.find_one({"user.email": email, "address.is_delivery": True})
        if not address:
            return {"message": "Usuário não possui endereço de entrega cadastrado"}
        # TODO
        db.cart_db.aggregate([
            {"$match": { "user.email": email}},
            {"$merge": {"into": "order"}},
            {"$addFields": {"address": dict(address)}}
        ])
        return {"message": "vixi maria"}
            
        # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')