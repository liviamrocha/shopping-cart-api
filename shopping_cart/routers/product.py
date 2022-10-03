from fastapi import APIRouter
from shopping_cart.schemas.product import ProductSchema
from shopping_cart.cruds.product import create_product

router = APIRouter(tags=['Products'], prefix='/products')


# Criar um produto
@router.post('')
async def post_product(product: ProductSchema):
    message = await create_product(product)
    return message
