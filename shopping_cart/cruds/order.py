from pydantic import EmailStr
from shopping_cart.schemas.order import order_helper
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
            print(f'create_order.error: {e}')


# Consultar pedidos por e-mail
async def find_orders(email: EmailStr):
    try:
        # Valida se o cliente possui um pedido no database
        find_user = await db.order_db.find_one({"user.email": email})
        if not find_user:
            return {"message": "Usuário não encontrado"}
        # Busca todos os pedidos no database
        orders_cursor = db.order_db.find({"user.email": email})
        # Transforma o objeto em lista
        orders_list = await orders_cursor.to_list(length=100)
        # Order_helper remove do retorno o password e o is_admin
        return order_helper(orders_list)
# Retona a mensagem de erro
    except Exception as e:
            print(f'find_orders.error: {e}')


# Consultar produtos e suas quantidades em pedidos
async def find_product_quantity(email: EmailStr):
    try:
        # Valida se o cliente possui um pedido no database
        find_user = await db.order_db.find_one({"user.email": email})
        if not find_user:
            return {"message": "Usuário não encontrado"}
        # Busca todos os pedidos no database
        orders_cursor = db.order_db.find({"user.email": email})
        # Transforma o objeto em lista
        orders_list = await orders_cursor.to_list(length=100)
        # cria uma lista com produtos e quantidades
        order_item_list = []
        for item in orders_list:
            for order in item["order_items"]:
                order_item_list.append(order)
        # Retorna a lista
        return order_item_list
# Retona a mensagem de erro
    except Exception as e:
            print(f'find_product_quantity.error: {e}')
            

# Consultar quantos carrinhos fechados o cliente possui
async def count_orders(email: EmailStr):
    try:
        # Valida se o cliente possui um pedido no database
        find_user = await db.order_db.find_one({"user.email": email})
        if not find_user:
            return {"message": "Usuário não encontrado"}
        # Busca a quantidade de pedidos do usuário
        orders_count = await db.order_db.count_documents({"user.email": email})
        return {"message": f"Total de pedidos: {orders_count}"}
# Retona a mensagem de erro
    except Exception as e:
            print(f'count_orders.error: {e}')