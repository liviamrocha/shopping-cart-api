import uuid
from pydantic import EmailStr
from datetime import datetime
from bson.binary import UuidRepresentation
from shopping_cart.server.database import db

# Necessário para serializar documentos com ObjectId
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str


async def create_order(email: EmailStr, delivery_address: dict, order_id: str):
    copy_cart = db.cart_db.aggregate([
        {"$match": { "user.email": email}},
        {"$addFields": {
            "address": delivery_address, 
            "order_id": order_id,
            "created_at": datetime.now() ,
            "updated_at": datetime.now()
        }},
        {"$merge": {"into": "order"}}
    ])
    return await copy_cart.to_list(length=100)

async def update_payment_status(email: EmailStr):
    updated_status = await db.cart_db.find_one_and_update(
        {"user.email": email},
        {"$set": {"paid": True, "updated_at": datetime.now()}}
    )
    return updated_status

async def find_user_order(email: EmailStr):
    find_user_order = await db.order_db.find_one({"user.email": email})
    return find_user_order

# Consultar pedidos por e-mail
async def get_orders(email: EmailStr):

    orders_cursor = db.order_db.find({"user.email": email})
    orders = [
        product
        async for product in orders_cursor
    ]
    return orders

# Retornar order por id
async def get_order_by_id(order_id: int):
    find_user_order = await db.order_db.find_one({"order_id": order_id})
    return find_user_order

# Consultar produtos e suas quantidades em pedidos
async def get_itens_from_order(email: EmailStr, order_id: str):
    orders_cursor = db.order_db.find({
        "user.email": email,
        "order_id": order_id
    })
    orders_list = await orders_cursor.to_list(length=100)
    order_item_list = []
    for item in orders_list:
        for order in item["items"]:
            order_item_list.append(order)
    return order_item_list

        
# Consultar quantos carrinhos fechados o cliente possui
async def get_orders_count(email: EmailStr):
    orders_count = await db.order_db.count_documents({"user.email": email})
    return orders_count

# Checa se existe uma order específica associada ao usuário
async def validade_order_for_user(email: EmailStr, order_id: str):
    find_user_order = await db.order_db.find_one({
        "user.email": email,
        "order_id": order_id
    })
    return find_user_order