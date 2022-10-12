from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from shopping_cart.schemas.order_items import OrderItemSchema
from shopping_cart.schemas.user import UserSchema


class CartSchema(BaseModel):
    user: UserSchema
    items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    paid: bool = Field(default=False)
    created_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora de criação do carrinho"
    )
    updated_at: datetime = Field(
        default=datetime.now(),
        description="Data/hora da última atualização"
    )
class CartRequestSchema(BaseModel):
    product_id: int = Field(description="ID do produto")
    quantity: int = Field(gt=0, description="ID do produto")
class CartResponseSchema(BaseModel):
    items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    

        
    
    