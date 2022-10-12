from math import prod
from pydantic import EmailStr
from shopping_cart.schemas.product import ProductSchema
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.cart import CartRequestSchema, CartSchema, cart_helper
from shopping_cart.schemas.order_item import OrderItemSchema, order_item_helper
from shopping_cart.server.database import db



# Cria um carrinho 
async def create_cart(user: UserSchema):
    cart = CartSchema(user=dict(user)).dict()
    added_cart = await db.cart_db.insert_one(cart)
    return added_cart

# Adiciona um produto
async def add_to_cart(email: EmailStr, cart_item: dict):
    added_item = await db.cart_db.find_one_and_update(
        {"user.email": email},
        {"$addToSet": {"order_items": cart_item}}
    )
    return added_item


# Deleta item do carrinho
async def delete_cart_item(email: EmailStr, product_code: int):
    print('chamou o delete')
    deleted_item = await db.cart_db.find_one_and_update(
        {"user.email": email},
        {"$pull": {"order_items": {"product.code": product_code}}}
    )

# Checa se o item já existe dentro do carrinho
async def check_cart_item(email, product_id):
    cart_document = await db.cart_db.find_one(
        {"user.email": email, "order_items.product.code": product_id}
    )
    return cart_document

# Deleta (limpa) carriho
async def delete_cart(email: EmailStr):
    deleted_cart = await db.cart_db.find_one_and_delete({"user.email": email})

# Atualiza quantidade de um item no carrinho
async def update_item_quantity(
    email: EmailStr,
    product_id: int,
    index: int,
    new_quantity: int
) -> bool:

    print('Vim pra cá')
    updated_cart = await db.cart_db.find_one_and_update(
        {"user.email": email, "order_items.product.code": product_id},
        {"$set": {f"order_items.{index}.quantity": new_quantity}}
    )
    return updated_cart  
            

# Atualiza preço total do carrinho
async def update_total_price(email: EmailStr, new_total_price: float):
    cart = await db.cart_db.find_one_and_update(
        {"user.email": email},
        {"$set": {"total_price": new_total_price}}
    )
    return cart

# Atualiza preço total do carrinho
async def update_total_quantity(email: EmailStr, new_total_quantity: int):
    cart = await db.cart_db.find_one_and_update(
        {"user.email": email},
        {"$set": {"total_quantity": new_total_quantity}}
    )
    return cart


# Remove um produto do carrinho
# async def remove_product_cart(email: EmailStr, code: int, quantity: int):
#         try:
#             # Verifica se o usuário possui um carrinho
#             find_cart = await db.cart_db.find_one({"user.email": email})
#             if not find_cart:
#                 return {"message": "Usuário não possui um carrinho"}
#             if find_cart:
#                 product_exists = await db.cart_db.find_one({"user.email": email, "order_items.product.code": code})
#                 if not product_exists:
#                     return {"message": "Produto não encontrado"}
#             # Valida se o carrinho possui a quantidade a ser removida
#             quantity_req = 0
#             for item in find_cart["order_items"]:
#                 if item["product"]["code"] == code:
#                     quantity_req = item["quantity"]
#             if quantity_req < quantity:
#                 return {"message": "Quantidade superior à existente no carrinho"}
            
        
#             # Valida se o produto existe - necessário para funções de quantidade total e valor total
#             validate_product = await db.product_db.find_one({"code": code})
#             if not validate_product:
#                 return {"message": "O produto não existe"}
            
#             # Valida se o produto já existe no carrinho
#             product_exists = await db.cart_db.find_one({"user.email": email, "order_items.product.code": code})
#             if product_exists:
#                 for item in product_exists["order_items"]:
#                     # Verifica se o produto existe no carrinho e se a quantidade disponível é maior que a quantidade que deseja remover
#                     if item["product"]["code"] == code and item["quantity"] > quantity:
#                         index = 0 
#                         for item in product_exists["order_items"]:
#                             if item["product"]["code"] == code:
#                                 new_quantity = item["quantity"] - quantity
#                                 await db.cart_db.find_one_and_update(
#                                     {"user.email": email, "order_items.product.code": code},
#                                     {"$set": {f"order_items.{index}.quantity": new_quantity}})
#                             index += 1
#                     # Caso a quantidade que deseja remover seja igual à do carrinho, remove o produto
#                     else:        
#                         order_item = OrderItemSchema()
#                         order_item.product = validate_product
#                         order_item.quantity = quantity
#                         # Remove o produto do carrinho
#                         await db.cart_db.find_one_and_update(
#                             {"user.email": email},
#                             {"$pull": {"order_items": order_item.dict()}})
#             # Altera a quantidade total e a soma do carrinho
#             else:
#                 order_item = OrderItemSchema()
#                 order_item.product = validate_product
#                 order_item.quantity = quantity
#             await db.cart_db.find_one_and_update(
#                 {"user.email": email},
#                 [{"$set": {"total_price": find_cart["total_price"] - validate_product["price"] * quantity}},
#                 {"$set": {"total_quantity": find_cart["total_quantity"] - quantity}}]
#             )
            
#             # Verifica se o carrinho está vazio e deleta o carrinho
#             find_product = await db.cart_db.find_one({"user.email": email})
#             if find_product["total_quantity"] == 0:
#                 await db.cart_db.find_one_and_delete({"user.email": email})
                
#             # Retorna a mensagem do produto removido
#             return {"message": "Produto removido do carrinho"}
        
#         # Retona a mensagem de erro
#         except Exception as e:
#                 print(f'remove_product_from_cart.error: {e}')
                
# Verifica se o usuário possui carrinho cadastrado
async def get_user_cart(email: EmailStr):
    cart = await db.cart_db.find_one({"user.email": email})
    return cart

# Retorna o carrinho do usuário
async def find_cart_by_email(email: EmailStr) -> dict:
    cart = await db.cart_db.find_one({"user.email": email})
    return cart
        