from typing import List, Optional
from pydantic import BaseModel, Field
from shopping_cart.schemas.user import UserSchema


class AddressSchema(BaseModel):
    street: str = Field(
        min_length=3, 
        max_length=200,
        description="Nome da rua ou avenida"
    )
    zip_code: str = Field(
        description="CEP"
    )
    number: int = Field(
        description="Número do local"
    )
    city: str = Field(
        min_length=3, 
        max_length=200,
        description="Nome da cidade"
    )
    state: str = Field(
        min_length=3, 
        max_length=200,
        description="Nome do estado"
    )
    is_delivery: bool = Field(
        description="Endereço de entrega?"
    )
    complement: Optional[str] = Field(
        description="Ex: Bloco/Apartamento"
    )
class AddressUpdateSchema(AddressSchema):
    pass

