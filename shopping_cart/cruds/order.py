from gettext import find
from shopping_cart.schemas.address import AddressSchema
from shopping_cart.schemas.user import UserSchema
from shopping_cart.server.database import db




# Transforma um carrinho em um pedido
async def create_order(user: UserSchema):
    try:
        # Busca o carrinho no database
        find_cart = await db.cart_db.find_one({"user.email": user.email})
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        return {"message": "deu certo"}
        
        
        # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')