import logging
from motor.motor_asyncio import AsyncIOMotorClient
from shopping_cart.core import settings

env = settings.get_environment_variables()
URI = f"mongodb+srv://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}@{env.CLUSTER_NAME}/{env.DATABASE_NAME}?retryWrites={env.RETRY}&w={env.W}"


class Database():
    client: AsyncIOMotorClient = None
    product_db = None
    user_db = None
    address_db = None
    order_db = None
    order_item_db = None
    cart_db = None
    
    
db = Database()

async def connect_db():
    db.client = AsyncIOMotorClient(
        URI, 
        maxPoolSize=10, 
        minPoolSize=10
    )
    db.product_db = db.client.shopping_cart.product
    db.user_db = db.client.shopping_cart.user
    db.address_db = db.client.shopping_cart.address
    db.order_db = db.client.shopping_cart.order
    db.order_item_db = db.client.shopping_cart.order_item
    db.cart_db = db.client.shopping_cart.cart
    
    logging.info('Connect to database')
    
async def close_conn_db():
    db.client.close()
