from typing import List
from fastapi import APIRouter, Depends, status
from shopping_cart.schemas.product import (
    ProductSchema, 
    ProductUpdateSchema, 
    ProductResponse
)
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.controllers.product import (
    insert_new_product,
    get_all_products,
    search_product_by_name,
    search_product_by_id,
    update_product_by_id,
    delete_product_by_id
)
from shopping_cart.schemas.user import UserSchema


router = APIRouter(tags=['Products'], prefix='/products')

@router.post(
    '/', 
    summary="Create product",
    description="Registration of a new product",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponse
)
async def post_product(product: ProductSchema, current_user: UserSchema = Depends(get_current_user)):
    new_product = await insert_new_product(product)
    return new_product


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponse],
    summary="Get all registered products.",
    description="Search for all registered products.",

)
async def get_products(current_user: UserSchema = Depends(get_current_user)) -> List[ProductResponse]:
    products = await get_all_products()
    return products


@router.get(
    '/name',
    status_code=status.HTTP_200_OK,
    response_model=List[ProductResponse],
    summary="Get product by name",
    description="Search for a product by name",
)
async def get_product_by_name(name: str, current_user: UserSchema = Depends(get_current_user)):
    product = await search_product_by_name(name)
    return product


@router.get(
    '/id',
    status_code=status.HTTP_200_OK,
    response_model=ProductResponse,
    summary="Get product by code",
    description="Search for a product by code",
)
async def get_product_by_id(id: int, current_user: UserSchema = Depends(get_current_user)):
    product = await search_product_by_id(id)
    return product


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED, 
    response_model=ProductResponse,
    summary="Update product",
    description="Update product by code",
) 
async def put_product(id: int, product_data: ProductUpdateSchema, current_user: UserSchema = Depends(get_current_user)): 
    return await update_product_by_id(id, product_data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete product",
    description="Remove a product by id",
)
async def delete_product(id: int, current_user: UserSchema = Depends(get_current_user)):
    return await delete_product_by_id(id)