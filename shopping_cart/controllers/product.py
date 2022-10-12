from typing import List, Optional
import shopping_cart.cruds.product as product_crud
from shopping_cart.schemas.product import (
    ProductSchema, 
    ProductUpdateSchema, 
    ProductResponse
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
    DataConflictException
)


async def validate_product(product: ProductSchema, input_code: Optional[str] = None):

    is_new_product = input_code is None

    input_product = await product_crud.product_by_id(product.code)

    if input_product is not None and is_new_product:
        raise AlreadyExistException("Cannot create product. A product with the same code already exists")
        

async def insert_new_product(product: ProductSchema) -> ProductResponse:

    await validate_product(product)

    new_product = product.dict()
    await product_crud.create_product(new_product)
    created_product = ProductResponse(**new_product)

    return created_product


async def get_all_products() -> List[dict]:
    products = await product_crud.list_products()
    return products


async def search_product_by_name(
    product_name: str, 
    raise_exception: bool = True
) -> Optional[dict]:

    products = await product_crud.product_by_name(product_name)

    if not products and raise_exception:
        raise NotFoundException('Product not found')

    return products


async def search_product_by_id(
    code: int, 
    raise_exception: bool = True
) -> Optional[dict]:

    product = await product_crud.product_by_id(code)

    if not product and raise_exception:
        raise NotFoundException('Product not found')

    return product


async def update_product_by_id(code: int, product_data: ProductUpdateSchema) -> ProductResponse:

    await search_product_by_id(code)

    if product_data.code is not None and product_data.code != code:
        raise DataConflictException('The codes are different')

    await validate_product(product_data, code)

    product_to_update = product_data.dict()

    if product_data.code is None:
        product_to_update.pop('code', None)

    await product_crud.update_product(code, product_to_update)
    updated_product = await search_product_by_id(code)

    return updated_product

async def delete_product_by_id(code: int) -> ProductResponse:
    removed = await product_crud.remove_product(code)
    if not removed:
        raise NotFoundException('Product not found')
    return "Product successfully deleted"

async def update_product_inventory(order):
    for item in order['items']:
        await product_crud.update_inventory(item['product']['code'], item["quantity"])