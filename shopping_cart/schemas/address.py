from typing import List, Optional
from uuid import uuid1
from datetime import datetime
from pydantic import BaseModel, Field


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

    class Config:
        schema_extra = {
            "example": {
                "street": "string",
                "zip_code": "string",
                "number": 0,
                "city": "string",
                "state": "string",
                "is_delivery": True,
                "complement": "string"
            }
        }

class AddressResponseSchema(BaseModel):
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
    created_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora de criação do endereço"
    )
    update_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora da última atualização"
    )
    