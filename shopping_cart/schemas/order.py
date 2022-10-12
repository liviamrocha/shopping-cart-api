from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from shopping_cart.schemas.address import AddressSchema
from shopping_cart.schemas.cart import CartSchema
from shopping_cart.schemas.product import ProductSchema
from shopping_cart.schemas.order_items import OrderItemSchema



class OrderSchema(BaseModel):
    order_number: UUID = Field(default_factory=uuid4)
    cart: CartSchema
    address: AddressSchema

class OrderItemSchema(BaseModel):
    product: ProductSchema 
    quantity: int 
    
class OrderResponseSchema(BaseModel):
    order_id: str = Field(description="Número do pedido")
    address: AddressSchema = Field(description="Endereço de entrega")
    paid: bool = Field(description="Pedido pago?")
    total_price: float = Field(description="Valor total do pedido")
    total_quantity: int = Field(description="Quantidade de produtos")
    items: List[OrderItemSchema] = Field(description="Itens do pedido")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
