

from typing import Optional
from pydantic import BaseModel
from shopping_cart.schemas.product import ProductSchema


class OrderItemSchema(BaseModel):
    product: Optional[ProductSchema]
    quantity: int = 0
    