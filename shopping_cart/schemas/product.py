from pydantic import BaseModel, Field
from typing import Optional
from shopping_cart.schemas.utils import AllOptional

class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float
    image: str
    code: int 

class ProductUpdateSchema(ProductSchema, metaclass=AllOptional):
    pass
class ProductResponse(ProductSchema):
    pass



