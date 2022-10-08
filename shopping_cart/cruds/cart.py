from pydantic import EmailError, EmailStr
from shopping_cart.schemas.cart import CartSchema, cart_helper
from shopping_cart.schemas.order_item import OrderItemSchema
from shopping_cart.schemas.user import UserSchema
from shopping_cart.server.database import db



# Cria um carrinho 
async def create_cart(cart: CartSchema): 
    try:
        # Verifica se o usuário já possui um carrinho
        find_cart = await db.cart_db.find_one({"user.email": cart.user.email})
        print(find_cart)
        if find_cart:
            return {"message": "Usuário já possui um carrinho"}
        # Cria um novo carrinho
        add_cart = await db.cart_db.insert_one(cart.dict())
        # Valida e retorna a mensagem
        if add_cart.inserted_id:
            return {"message": "Carrinho cadastrado com sucesso"}
        
    # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')
            
            
# Adiciona um produto
async def add_product_cart(user: UserSchema, order_item: OrderItemSchema):
    try: 
        # Verifica se o usuário possui um carrinho
        find_cart = await db.cart_db.find_one({"user.email": user.email})
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        
        # Valida se o produto existe
        validate_product = await db.product_db.find_one({"order_item.product": order_item.product})
        if not validate_product or order_item.product.stock == 0:
            return {"message": "O produto não está disponível"}
        
        # Caso existe carrinho e o produto esteja disponível, adiciona ao carrinho
        await db.cart_db.find_one_and_update(
            {"user.email": user.email},
            {"$addToSet": {"products": dict(order_item.product)}},
            {"$sum": {"total_quantity": order_item.quantity}}
            # Total price????
        
        )
        # Retona a mensagem de erro
    except Exception as e:
            print(f'add_product_to_cart.error: {e}')
            
            
# Remove um produto do carrinho
async def remove_product_cart(user: UserSchema, order_item: OrderItemSchema):
        try:
            # Verifica se o usuário possui um carrinho
            find_cart = await db.cart_db.find_one({"user.email": user.email})
            if not find_cart:
                return {"message": "Usuário não possui um carrinho"}
            # Caso existe carrinho, retira o produto
            # await db.cart_db.find_one_and_delete(
            #     {"user.email": user.email},
            #     {"$addToSet": {"products": dict(order_item.product)}},
            #     {"$sum": {"total_quantity": order_item.quantity}}
            #     # Total price????
            
            # )
            # # Retona a mensagem de erro
        except Exception as e:
                print(f'add_product_to_cart.error: {e}')
                

# Retorna o carrinho do usuário
async def find_cart_by_email(email: EmailStr):
    try:
        find_cart = await db.cart_db.find_one({"user.email": email})
        print(find_cart)
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        return cart_helper(find_cart)
    except Exception as e:
                print(f'find_cart_by_email.error: {e}')