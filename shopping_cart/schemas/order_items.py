from typing import List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from shopping_cart.schemas.product import ProductSchema


class OrderItemSchema(BaseModel):
    product: ProductSchema
    quantity: int