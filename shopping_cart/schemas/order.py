

import json
from operator import itemgetter
from pydantic import BaseModel

from shopping_cart.schemas.address import Address
from shopping_cart.schemas.cart import CartSchema
from shopping_cart.schemas.order_item import OrderItemSchema


class OrderSchema(BaseModel):
    cart: CartSchema
    address: Address
    
def order_helper(order):
    for item in order:
        del item["user"]["password"]
        del item["user"]["is_admin"]
    return order
    
    
    
    
def order_helper_list(order):
    order_items_list = []
    for item in order["order_items"]:
        order_items_list.append(item)
    return {
        "order_items": order_items_list
    }
