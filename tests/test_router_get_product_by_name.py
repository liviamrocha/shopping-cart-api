import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


@patch("shopping_cart.cruds.product.product_by_name")
def test_router_get_product_by_name(mock_prod):
    mock_prod.return_value = [{
    "code": 12346,
    "name": "Barbie",
    "description": "Boneca de plástico",
    "price": 150,
    "stock": 10,
    "inmetro": "null",
    "age_group": "null",
    "brand": "null",
    "material": "null",
    "height_dimension": 1.5,
    "width_dimension": 1.5,
    "length_dimension": 1,
    "image": "umabarbie.jpg",
    "guarantee": "null",
    "cor": "null",
    "topic": "null",
    "cartoon_character": "null",
    "best_uses": "null"  
  }]
    respost = client.get("/products/name?name=Barbie")
    assert respost.status_code == 200