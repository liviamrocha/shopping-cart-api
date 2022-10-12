from pydantic import BaseModel, Field
from typing import Optional
from shopping_cart.schemas.utils import AllOptional

class ProductSchema(BaseModel):
    code: int = Field(description="Código do produto")
    name: str = Field(max_length=100, description="Nome do produto")
    description: str = Field(description="Descrição do produto")
    price: float = Field(gt=0.01, description="Preço do produto")
    stock: int = Field(gt=0, description="Quantidade disponível no estoque")
    inmetro: Optional[str] = Field(description="Código de certificação do brinquedo no INMETRO")
    age_group: Optional[str] = Field(description="Faixa etária recomendada")
    brand: Optional[str] = Field(description="Marca do brinquedo")
    material: Optional[str] = Field(description="Tipo de material do brinquedo")
    height_dimension: Optional[float] = Field(description="Altura do brinquedo")
    width_dimension: Optional[float] = Field(description="Largura do brinquedo")
    length_dimension: Optional[float]	= Field(description="Comprimento do brinquedo")
    image: Optional[str] = Field(description="Imagem do produto")
    guarantee: Optional[str] = Field(description="Garantia do produto")
    cor: Optional[str] = Field(description="Cor do produto")
    topic: Optional[str] = Field(description="Tema do brinquedo")
    cartoon_character: Optional[str] = Field(description="Personagem de desenho animado")
    best_uses: Optional[str] = Field(description="Melhores usos para o brinquedo")

    # Configurações extra para o Swagger
    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "price": 0.01,
                "image": "string",
                "code": 1,
                "name": "string",
                "description": "string",
                "price": 0.01,
                "stock": 1,
                "inmetro": "string",
                "age_group": "string",
                "brand": "string",
                "material": "string",
                "height_dimension": "string",
                "width_dimension": "string",
                "length_dimension": "string",
                "image": "string",
                "guarantee": "string",
                "cor": "string",    
                "topic": "string",
                "cartoon_character": "string",
                "best_uses": "string"
            }
        }

class ProductUpdateSchema(ProductSchema, metaclass=AllOptional):
    price: float = Field(gt=0.01)

   # Configurações extra para o Swagger 
    class Config:
        schema_extra = {
            "example": {
                "name": "string",
                "description": "string",
                "price": 0.01,
                "image": "string",
                "name": "string",
                "description": "string",
                "price": 0.01,
                "stock": 1,
                "inmetro": "string",
                "age_group": "string",
                "brand": "string",
                "material": "string",
                "height_dimension": "string",
                "width_dimension": "string",
                "length_dimension": "string",
                "image": "string",
                "guarantee": "string",
                "cor": "string",    
                "topic": "string",
                "cartoon_character": "string",
                "best_uses": "string"
            }
        }
class ProductResponse(ProductSchema, metaclass=AllOptional):
    pass
