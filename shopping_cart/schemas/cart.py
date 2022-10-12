from typing import List
from pydantic import BaseModel, Field
from shopping_cart.schemas.order_items import OrderItemSchema
from shopping_cart.schemas.user import UserSchema


class CartSchema(BaseModel):
    user: UserSchema
    order_items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    paid: bool = Field(default=False)
class CartRequestSchema(BaseModel):
    product_id: int
    quantity: int
class CartResponseSchema(BaseModel):
    order_items: List[OrderItemSchema] = []
    total_quantity: int = 0
    total_price: float = 0
    

        
    
    