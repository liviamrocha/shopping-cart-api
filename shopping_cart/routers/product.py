from fastapi import APIRouter, HTTPException, status
from shopping_cart.schemas.product import ProductSchema, ProductUpdateSchema, ProductResponse
from shopping_cart.cruds.product import (
    create_product,
    list_products,
    product_by_id,
    product_by_name,
    update_product,
    remove_product
)

router = APIRouter(tags=['Products'], prefix='/products')

@router.post('', status_code=status.HTTP_201_CREATED)
async def post_product(product: ProductSchema):
    return await create_product(product)

@router.get('')
async def get_products():
    products = await list_products()
    return products

@router.get('/name', response_model=ProductResponse)
async def get_product_by_name(name: str):
    product = await product_by_name(name)
    print(product)
    return product

@router.get('/id', response_model=ProductResponse)
async def get_product_by_id(id: int):
    product = await product_by_id(id)
    return product

@router.put('/id', status_code=status.HTTP_201_CREATED) # Adicioanr response model
async def put_product(id: int, product_data: ProductUpdateSchema): 
    return await update_product(id, product_data)

@router.delete('/id')
async def delete_product(id: int):
    return await remove_product(id)