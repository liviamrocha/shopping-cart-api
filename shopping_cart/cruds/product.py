from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from shopping_cart.server.database import db


async def create_product(product: dict) -> dict:
    new_product = await db.product_db.insert_one(product)
    return new_product

    
async def list_products():
    product_cursor = db.product_db.find()
    products = [
        product
        async for product in product_cursor
    ]
    return products


async def product_by_id(code: int) -> Optional[dict]:
    product = await db.product_db.find_one({"code": code})
    return product


async def product_by_name(name: str):
    product_cursor = db.product_db.find({"name": {'$regex':f'^{name}'}})
    products = [
        product
        async for product in product_cursor
    ]  
    return products
    
            
async def update_product(code: int, product_data: dict) -> bool:
    data = {key: value for key, value in dict(product_data).items() if value is not None}
    data['updated_at'] = datetime.now()

    product = await db.product_db.update_one(
        {'code': code},
        {'$set': data}
    )
    return product.modified_count == 1


async def remove_product(code: int) -> bool:
    product = await db.product_db.delete_one(
        {'code': code}
    )
    return product.deleted_count > 0
    
   
async def update_inventory(product_id: int, quantity: int):

    current_product = await product_by_id(product_id)
    current_stock = current_product['stock']
    new_stock = current_stock - quantity

    if new_stock < 0:
        new_stock = 0

    product = await db.product_db.update_one(
        {"code": product_id},
        {"$set": {"stock": new_stock, "updated_at": datetime.now()}}
    )
    return product.modified_count == 1