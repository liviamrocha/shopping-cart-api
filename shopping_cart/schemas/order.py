

import json
from operator import itemgetter
from pydantic import BaseModel

from shopping_cart.schemas.address import Address
from shopping_cart.schemas.cart import CartSchema


class OrderSchema(BaseModel):
    cart: CartSchema
    address: Address
    
def order_helper(order):
    for item in order:
        del item["user"]["password"]
        del item["user"]["is_admin"]
    return order
    
    
    
    
def order_helper_list(order) -> dict:
    order_list = { 
        "id": str(order["_id"]),
        "name": order["user"]["name"],
        "email": order["user"]["email"],
        "password": order["user"]["password"],
        "is_active": order["user"]["is_active"],
        "is_admin": order["user"]["is_admin"],
        "created_at": order["user"]["created_at"],
        "order_items": order["order_items"],
        "total_quantity": order["total_quantity"],
        "total_price": order["total_price"],
        "paid": order["paid"],
    }
    for item in order:
        order_list.append(item)
    return order_list