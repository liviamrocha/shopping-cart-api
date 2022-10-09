from typing import List, Optional
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
   
async def update_inventory(product_id: int, quantity: int, increment: bool):

    if not increment:
        quantity = -quantity

    product = await db.product_db.update_one(
        {'code': product_id},
        {'$inc': { "stock": quantity }}
    )

    return product.modified_count == 1
