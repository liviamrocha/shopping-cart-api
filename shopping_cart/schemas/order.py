

from pydantic import BaseModel

from shopping_cart.schemas.address import Address
from shopping_cart.schemas.cart import CartSchema


class OrderSchema(BaseModel):
    cart: CartSchema
    address: Address