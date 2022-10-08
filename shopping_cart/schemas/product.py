from pydantic import BaseModel, Field
from typing import Optional
from shopping_cart.schemas.utils import AllOptional

class ProductSchema(BaseModel):
    name: str = Field(max_length=100, description="Nome do produto")
    description: str = Field(description="Descrição do produto")
    price: float = Field(gt=0.01, description="Preço do produto")
    image: str = Field(description="Imagem do produto")
    code: int = Field(description="Código do produto")

    # Configurações extra para o Swagger
    class Config:
        schema_extra = {
            "example": {
                "name": "Produto 1",
                "description": "Descrição do produto 1",
                "price": 10.99,
                "image": "produto1.jpeg",
                "code": 1
            }
        }

class ProductUpdateSchema(ProductSchema, metaclass=AllOptional):
    price: float = Field(gt=0.01)
class ProductResponse(ProductSchema):
    pass

    