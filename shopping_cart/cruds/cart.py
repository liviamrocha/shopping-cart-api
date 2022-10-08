from gettext import find
from wsgiref import validate
from pydantic import EmailStr
from shopping_cart.schemas.cart import CartSchema, cart_helper
from shopping_cart.schemas.order_item import OrderItemSchema
from shopping_cart.schemas.user import UserSchema
from shopping_cart.server.database import db



# Cria um carrinho 
async def create_cart(cart: CartSchema): 
    try:
        # Verifica se o usuário já possui um carrinho
        find_cart = await db.cart_db.find_one({"user.email": cart.user.email})
        if find_cart:
            return {"message": "Usuário já possui um carrinho"}
        # Cria um novo carrinho
        print(cart)
        add_cart = await db.cart_db.insert_one(cart.dict())
        # Valida e retorna a mensagem
        if add_cart.inserted_id:
            return {"message": "Carrinho cadastrado com sucesso"}
        
    # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')
            
            
# Adiciona um produto
async def add_product_cart(email: EmailStr, code: int, quantity: int):
    try: 
        # Verifica se o usuário possui um carrinho
        find_cart = await db.cart_db.find_one({"user.email": email})
        if not find_cart:
            return {"message": "Usuário não possui um carrinho"}
        
        # Valida se o produto existe e o retorna
        validate_product = await db.product_db.find_one({"code": code})
        if not validate_product: #or validate_product.stock == 0:
            return {"message": "O produto não está disponível"}
        
        order_item = OrderItemSchema()
        order_item.product = validate_product
        order_item.quantity = quantity
        
        # Caso exista carrinho e o produto esteja disponível, adiciona ao carrinho
        await db.cart_db.find_one_and_update(
            {"user.email": email},
            {"$addToSet": {"order_items": order_item.dict()}})
        await db.cart_db.find_one_and_update(
            {"user.email": email},
            [{"$set": {"total_price": find_cart["total_price"] + validate_product["price"] * quantity}},
            {"$set": {"total_quantity": find_cart["total_quantity"] + quantity}}]
        )
        return {"message": "Produto adicionado ao carrinho"}
    
    # Retona a mensagem de erro
    except Exception as e:
            print(f'add_product_to_cart.error: {e}')
            
            
# Remove um produto do carrinho
async def remove_product_cart(email: EmailStr, code: int, quantity: int):
        try:
            # Verifica se o usuário possui um carrinho
            find_cart = await db.cart_db.find_one({"user.email": email})
            if not find_cart:
                return {"message": "Usuário não possui um carrinho"}
            # Valida se o carrinho possui a quantidade a ser removida
            quantity_req = 0
            for item in find_cart["order_items"]:
                if item["product"]["code"] == code:
                    quantity_req = item["quantity"]
            if quantity_req < quantity:
                return {"message": "Quantidade superior à existente no carrinho"}
            
            # Valida se o produto existe
            validate_product = await db.product_db.find_one({"code": code})
            if not validate_product:
                return {"message": "O produto não existe"}
            
            order_item = OrderItemSchema()
            order_item.product = validate_product
            order_item.quantity = quantity
            
            # Remove o produto do carrinho
            await db.cart_db.find_one_and_update(
                {"user.email": email},
                {"$pull": {"order_items": order_item.dict()}})
            await db.cart_db.find_one_and_update(
                {"user.email": email},
                [{"$set": {"total_price": find_cart["total_price"] - validate_product["price"] * quantity}},
                {"$set": {"total_quantity": find_cart["total_quantity"] - quantity}}]
            )
            return {"message": "Produto removido do carrinho"}
        
        # Retona a mensagem de erro
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