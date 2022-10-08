

from pydantic import BaseModel
from shopping_cart.schemas.product import ProductSchema


class OrderItemSchema(BaseModel):
    product: ProductSchema
    quantity: int
    