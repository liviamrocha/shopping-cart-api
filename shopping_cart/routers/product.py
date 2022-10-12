from typing import List
from fastapi import APIRouter, status
from shopping_cart.schemas.product import (
    ProductSchema, 
    ProductUpdateSchema, 
    ProductResponse
)
from shopping_cart.controllers.product import (
    insert_new_product,
    get_all_products,
    search_product_by_name,
    search_product_by_id,
    update_product_by_id,
    delete_product_by_id
)


router = APIRouter(tags=['Products'], prefix='/products')

@router.post(
    '/', 
    summary="Create product",
    description="Registration of a new product",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse
)
async def post_product(product: ProductSchema):
    new_product = await insert_new_product(product)
    return new_product


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponse],
    summary="Get all registered products.",
    description="Search for all registered products.",

)
async def get_products() -> List[ProductResponse]:
    products = await get_all_products()
    return products


@router.get(
    '/name',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponse],
    summary="Get product by name",
    description="Search for a product by name",
)
async def get_product_by_name(name: str):
    product = await search_product_by_name(name)
    return product


@router.get(
    '/id',
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    summary="Get product by code",
    description="Search for a product by code",
)
async def get_product_by_id(id: int):
    product = await search_product_by_id(id)
    return product


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED, 
    response_model=ProductResponse,
    summary="Update product",
    description="Update product by code",
) 
async def put_product(id: int, product_data: ProductUpdateSchema): 
    return await update_product_by_id(id, product_data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete product",
    description="Remove a product by id",
)
async def delete_product(id: int):
    return await delete_product_by_id(id)