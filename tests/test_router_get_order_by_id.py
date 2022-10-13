from asyncio.windows_events import NULL
from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from main import app
from unittest.mock import patch
import pytest
client = TestClient(app)

@pytest.fixture
def client_authenticated():
    """
    Returns an API client which skips the authentication
    """
    def skip_auth():
        pass
    app.dependency_overrides[get_current_user] = skip_auth
    return TestClient(app)

@patch("shopping_cart.cruds.order.get_order_by_id")
def test_router_get_order_by_id(mock_id,client_authenticated):
    mock_id.return_value = {
        "order_id": "string",
        "address": {
    "street": "string",
    "zip_code": "string",
    "number": 0,
    "city": "string",
    "state": "string",
    "is_delivery": True,
    "complement": "string"
  },
  "paid": True,
  "total_price": 0,
  "total_quantity": 0,
  "items": [
    {
      "product": {
        "name": "string",
        "description": "string",
        "price": 1,
        "image": "string",
        "code": 1,
        "stock": 1,
        "inmetro": "string",
        "age_group": "string",
        "brand": "string",
        "material": "string",
        "height_dimension": 1,
        "width_dimension": 2,
        "length_dimension": 3,
        "guarantee": "string",
        "cor": "string",
        "topic": "string",
        "cartoon_character": "string",
        "best_uses": "string"
      },
      "quantity": 0
    }
  ],
  "created_at": "2022-10-12T22:32:05.140Z",
  "updated_at": "2022-10-12T22:32:05.140Z"
}
    respost = client_authenticated.get(f"/orders/id?order_id=c2710cd4-4a39-11ed-8522-00155d59380c")
    assert respost.status_code == status.HTTP_200_OK