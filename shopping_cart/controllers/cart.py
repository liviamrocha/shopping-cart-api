from typing import List, Optional
from operator import neg
from pydantic import EmailStr
import shopping_cart.cruds.cart as cart_crud
from shopping_cart.schemas.user import UserSchema
from shopping_cart.schemas.cart import (
    CartResponseSchema, 
    CartRequestSchema
)
from shopping_cart.controllers.exceptions.custom_exceptions import (
    NotFoundException,
    NotAvailableException,
    NotValidException
)
from shopping_cart.controllers.product import search_product_by_id
from shopping_cart.controllers.user import search_user_by_email


async def has_cart(email: EmailStr) -> bool:
    if not await cart_crud.get_user_cart(email):
        return False
    return True


async def validate_product(cart_data=CartRequestSchema, raise_exception=False) -> Optional[dict]:

    product = await search_product_by_id(cart_data.product_id)

    if product['stock'] < cart_data.quantity and raise_exception:
        raise NotAvailableException('Product not available for this quantity')
    return product


async def validate_item(email: EmailStr, product_id: int, raise_exception=False) -> Optional[dict]:

    cart = await cart_crud.check_cart_item(email, product_id)
    if not cart and raise_exception:
        raise NotAvailableException('Item not found')
    return cart


async def create_user_cart(user: dict) -> CartRequestSchema:
    await cart_crud.create_cart(UserSchema(**user))
    cart = await fetch_cart_by_email(user['email'])
    return cart


async def add_cart_item(email: EmailStr, cart_data: CartRequestSchema) -> Optional[dict]:

    user = await search_user_by_email(email)
    product = await validate_product(cart_data, raise_exception=True)

    if not await has_cart(email):
        cart = await create_user_cart(user)
    else:
        cart = await fetch_cart_by_email(email)

    cart_document = await validate_item(email, product['code'])
    if cart_document is not None:
        await update_item_quantity(email, cart_document, cart_data)
    else:
        cart_item = {
            'product': product,
            'quantity': cart_data.quantity
        }
        await cart_crud.add_to_cart(email, cart_item)

    await update_total_price(email, cart.total_price, product['price'], cart_data.quantity)
    await update_total_quantity(email, cart.total_quantity, cart_data.quantity)

    return {"message": "Product added to cart"}


async def remove_cart_item(email: EmailStr, cart_data: CartRequestSchema) -> Optional[dict]:
    
    if not await has_cart(email):
        raise NotFoundException("User's shopping cart is empty")

    cart = await validate_item(email, cart_data.product_id, raise_exception=True) 
    await validate_quantity_to_remove(cart, cart_data.product_id, cart_data.quantity) 
    product = await validate_product(cart_data) 
    
    for item in cart["items"]:
        if item["product"]["code"] == cart_data.product_id and item["quantity"] > cart_data.quantity:
            await update_item_quantity(email, cart, cart_data, increment=False)
        elif item["product"]["code"] == cart_data.product_id and item["quantity"] == cart_data.quantity:
            await cart_crud.delete_cart_item(email, cart_data.product_id)
        
    await update_total_price(email, cart['total_price'], product['price'], cart_data.quantity, increment=False)
    await update_total_quantity(email, cart['total_quantity'], cart_data.quantity, increment=False)
    await is_empty_cart(email)

    return {"message": "Product successfully deleted"}


async def clean_user_cart(email: EmailStr) -> Optional[dict]:
    await search_user_by_email(email)

    if not await has_cart(email):
        raise NotFoundException("User's shopping cart is already empty")
    await cart_crud.delete_cart(email)
    return {"message": "All items have been successfully removed"}


async def is_empty_cart(email):
    check_cart = await cart_crud.find_cart_by_email(email)
    if check_cart["total_quantity"] == 0:
        return await cart_crud.delete_cart(email)


async def validate_quantity_to_remove(cart: dict, product_id: int, quantity: int):
    document_quantity = 0

    for item in cart["items"]:
        if item["product"]["code"] == product_id:
            document_quantity = item["quantity"]

    if document_quantity < quantity:
        raise NotValidException(
            "Quantity entered is greater than the quantity in the cart"        
        )


async def update_item_quantity(
    email: EmailStr, 
    cart_document: dict, 
    cart_data: CartRequestSchema,
    increment: bool = True,
):
    quantity = cart_data.quantity
    if not increment:
        quantity = neg(quantity)

    index = 0
    for item in cart_document['items']:
        if item['product']['code'] == cart_data.product_id:
            new_quantity = item['quantity'] + quantity
            if new_quantity < 0:
                new_quantity = 0
            await cart_crud.update_item_quantity(email, cart_data.product_id, index, new_quantity)
        index += 1


async def update_total_price(
    email: EmailStr,
    current_total_price: float, 
    product_price: float, 
    quantity: int,
    increment: bool = True
):

    item_total_price = product_price * quantity
    if not increment:
        item_total_price = neg(item_total_price)

    new_total_price = current_total_price + item_total_price
    
    if new_total_price < 0:
        new_total_price = 0

    await cart_crud.update_total_price(email, new_total_price)

async def update_total_quantity(
    email: EmailStr,
    current_total_quantity: int, 
    quantity: int,
    increment: bool = True
):
    if not increment:
        quantity = - quantity

    new_total_quantity = current_total_quantity + quantity
    
    if new_total_quantity < 0:
        new_total_quantity = 0

    await cart_crud.update_total_quantity(email, new_total_quantity)

async def fetch_cart_by_email(email: EmailStr, raise_exception: bool = True) -> CartResponseSchema:

    await search_user_by_email(email)

    cart = await cart_crud.find_cart_by_email(email)
    if not cart and raise_exception:
        raise NotFoundException("User's shopping cart is empty")

    cart = {
        'items': cart['items'],
        'total_price': cart['total_price'],
        'total_quantity': cart['total_quantity'],
        'created_at': cart['created_at'],
        'updated_at': cart['updated_at']
    }
    return CartResponseSchema(**cart)


