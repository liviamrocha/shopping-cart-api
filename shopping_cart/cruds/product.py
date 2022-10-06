from shopping_cart.schemas.product import ProductSchema, ProductResponse
from bson import ObjectId
from shopping_cart.server.database import db


async def create_product(product: ProductSchema):
    try:
        product_exist = await db.product_db.find_one({"code": product.code})
        if product_exist:
            return {"message": "Produto já registrado"}
        
        product = await db.product_db.insert_one(product.dict())
        if product.inserted_id:
            return {"message": "Produto cadastrado"}
    except Exception as e:
            print(f'create_product.error: {e}')


async def list_products():
    try:
        product_cursor = db.product_db.find()
        products = [
            ProductResponse(**product)
            async for product in product_cursor
        ]
        return products
    except Exception as e:
            print(f'get_products.error: {e}')


async def product_by_id(code: int):
    try:
        product = await db.product_db.find_one({"code": code})
        print(product)
        if product:
            return ProductResponse(**product)
    except Exception as e:
        print(f'get_user_by_id.error: {e}')


async def product_by_name(name):
    try:
        product = await db.product_db.find_one({"name": name})
        if product:
            return ProductResponse(**product)
    except Exception as e:
            print(f'get_user_by_name.error: {e}')

            
async def update_product(code, product_data):
    try:
        data = {key: value for key, value in dict(product_data).items() if value is not None}

        product = await db.product_db.update_one(
            {'code': code},
            {'$set': data}
        )
        if product.modified_count:
            return True, product.modified_count
        return False, 0
    except Exception as e:
        print(f'update_product.error: {e}')


async def remove_product(code):
    try:
        product = await db.product_db.delete_one(
            {'code': code}
        )
        if product.deleted_count:
            return {'status': 'Product deleted'}
    except Exception as e:
        print(f'delete_product.error: {e}')