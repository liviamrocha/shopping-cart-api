from pydantic import EmailStr
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.cart import CartSchema
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
                
# Verifica se o usuário possui carrinho cadastrado
async def get_user_cart(email: EmailStr):
    cart = await db.cart_db.find_one({"user.email": email})
    return cart

# Retorna o carrinho do usuário
async def find_cart_by_email(email: EmailStr) -> dict:
    cart = await db.cart_db.find_one({"user.email": email})
    return cart
        