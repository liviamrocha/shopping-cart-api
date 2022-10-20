import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app

from unittest.mock import patch

client = TestClient(app)

class ExternalAPI():
  def __init__(self,status_code,response=None):
    self.status_code = status_code
    self.response = response
  def json(self):
    return self.response


@patch("shopping_cart.controllers.product.validate_product")
@patch("shopping_cart.cruds.product.create_product")
def test_router_add_product_fail(mock_get, mock_product):
  mock_get.return_value = ExternalAPI(201)
  mock_product.return_value = ExternalAPI(201,{
    "description": "str",
    "price": 1.5,
    "stock": 5,
    "inmetro": "Optional[str]",
    "age_group": "Optional[str]", 
    "brand": "Optional[str]",
    "material": "Optional[str]", 
    "height_dimension": 1, 
    "width_dimension": 1,
    "length_dimension": 1,	
    "image": "Optional[str]",
    "guarantee": "Optional[str]", 
    "cor": "Optional[str]", 
    "topic": "Optional[str] ",
    "cartoon_character": "Optional[str]", 
    "best_uses": "Optional[str]" 
})
  product = {
     "code": 12,
    "name": "str",
    "description": "str",
    "price": 1.5,
    "stock": 5,
    "inmetro": "Optional[str]",
    "age_group": "Optional[str]", 
    "brand": "Optional[str]",
    "material": "Optional[str]", 
    "height_dimension": 1, 
    "width_dimension": 1,
    "length_dimension": 1,	
    "image": "Optional[str]",
    "guarantee": "Optional[str]", 
    "cor": "Optional[str]", 
    "topic": "Optional[str] ",
    "cartoon_character": "Optional[str]", 
    "best_uses": "Optional[str]"
}
  respost = client.post("/products/", json=product)
  assert respost.status_code == status.HTTP_201_CREATED