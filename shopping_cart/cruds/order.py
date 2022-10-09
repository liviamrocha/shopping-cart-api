from pydantic import EmailStr
from shopping_cart.schemas.cart import cart_helper
from shopping_cart.schemas.order import order_helper, order_helper_list
from shopping_cart.schemas.order_item import order_item_helper
from shopping_cart.schemas.product import product_helper
from shopping_cart.server.database import db

# Necessário para serializar documentos com ObjectId
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


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
        
        # Encontra o primeiro endereço de entrega cadastrado
        for item in address["address"]:
            if item["is_delivery"] == True:
                delivery_address = item
                break
        
        # Troca o carrinho para pago, virando assim um pedido
        await db.cart_db.find_one_and_update(
            {"user.email": email},
            {"$set": {"paid": True}})
        
        # Copia o pedido para o database order
        copy_doc = db.cart_db.aggregate([
            {"$match": { "user.email": email}},
            {"$addFields": {"address": dict(delivery_address)}},
            {"$merge": {"into": "order"}}
        ])
        await copy_doc.to_list(length=100)
        
        # Deleta o carrinho do database cart
        await db.cart_db.find_one_and_delete({"user.email": email})
        
        # Retorna a mensagem do pedido criado
        return {"message": "Pedido criado com sucesso"}
            
    # Retona a mensagem de erro
    except Exception as e:
            print(f'create_cart.error: {e}')


# Consultar carrinhos fechados (pedidos) por e-mail
async def find_orders(email: EmailStr):
    # Busca todos os pedidos no database
    orders_cursor = db.order_db.find({"user.email": email})
    # Transforma o objeto em lista
    orders_list = await orders_cursor.to_list(length=100)
    # Order_helper remove do retorno o password e o is_admin
    return order_helper(orders_list)


# Consultar produtos e suas quantidades em pedidos
# TODO
async def find_product_quantity(email: EmailStr):
    product_list = []
    orders = await db.order_db.find({"user.email": email})
    print(orders)
    for item in orders["order_item"]:
        product_list.append(order_item_helper(item))
        
    return {"message": "deu"}


# Consultar quantos carrinhos fechados o cliente possui
# TODO
async def count_orders(email: EmailStr):
    orders_count = db.order_db.count_documents({"user.email": email})
    return {"message": "Total de pedidos: " + orders_count}
