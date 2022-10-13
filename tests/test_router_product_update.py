import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


@patch("shopping_cart.cruds.product.product_by_id")
@patch("shopping_cart.cruds.product.update_product")
def test_router_product_update(mock_id,mock_up):
  mock_id.retur_value = {
    "code": 2,
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
  mock_up.return_value = {
    "code": 2,
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
  product = {
     "code": 2,
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

  respost = client.put("/products/2",json= product)
  assert respost.status_code == status.HTTP_202_ACCEPTED







