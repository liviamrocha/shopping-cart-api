from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float
    image: str
    code: int 

class ProductUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    image: Optional[str]


# Modelo de retorno de um documento de product
def product_helper(product) -> dict:
    return{
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "image": product["image"],
        "code": product["code"],
    }


