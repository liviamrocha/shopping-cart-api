from fastapi import APIRouter
from shopping_cart.schemas.product import ProductSchema, ProductUpdateSchema
from shopping_cart.cruds.product import (
    create_product,
    list_products,
    product_by_id,
    product_by_name,
    update_product,
    remove_product
)

router = APIRouter(tags=['Products'], prefix='/products')

@router.post('')
async def post_product(product: ProductSchema):
    return await create_product(product)

@router.get('')
async def get_products():
    return await list_products()

@router.get('/name')
async def get_product_by_name(name: str):
    return await product_by_name(name)

@router.get('/id')
async def get_product_by_id(id: int):
    return await product_by_id(id)

@router.put('/id')
async def put_product(id: int, product_data: ProductUpdateSchema): 
    return await update_product(id, product_data)

@router.delete('/id')
async def delete_product(id: int):
    return await remove_product(id)