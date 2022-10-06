from pydantic import BaseModel, Field
from typing import Optional
from shopping_cart.schemas.utils import AllOptional

class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float = Field(gt=0.01)
    image: str
    code: int 

class ProductUpdateSchema(ProductSchema, metaclass=AllOptional):
    price: float = Field(gt=0.01)
class ProductResponse(ProductSchema):
    pass



