from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from shopping_cart.controllers.product import update_product_inventory
from main import app
from unittest.mock import patch
import pytest

class ExternalAPI():
  def __init__(self,status_code,response=None):
    self.status_code = status_code
    self.response = response
  def json(self):
    return self.response


@pytest.fixture
def client_authenticated():
    """
    Returns an API client which skips the authentication
    """
    def skip_auth():
        pass
    app.dependency_overrides[get_current_user] = skip_auth
    return TestClient(app)
    

    


@patch("shopping_cart.cruds.user.get_user_by_email")
@patch("shopping_cart.cruds.cart.get_user_cart")
@patch("shopping_cart.cruds.address.find_addresses_by_email")
@patch("shopping_cart.cruds.address.get_delivery_address")
@patch("shopping_cart.cruds.order.update_payment_status")
@patch("shopping_cart.cruds.order.create_order")
@patch("shopping_cart.cruds.cart.delete_cart")
@patch("shopping_cart.cruds.order.get_order_by_id")
def test_router_post_order(mock_user_by_email,mock_get_user_cart,mock_addresses_by_email,mock_get_delivery,
                            mock_update_payment,mock_create_order,mock_delete_cart,mock_get_order_by_id, client_authenticated):
    mock_user_by_email.return_value = {"email": "email"}
    mock_get_user_cart.return_value = {"user.email": "email"}
    mock_addresses_by_email.return_value = {"user.email": "email"}
    mock_get_delivery.return_value = {"user.email": "email",
            "address.is_delivery": True}
    mock_update_payment.return_value = {"user.email": "email",
                "paid": True}
    mock_create_order.return_value = { "user.email": "email",
              "address": "delivery_address",
                "order_id": "order_id" ,"into":"order"}
    mock_delete_cart.retur_value = {
    "order_id": "aec1b382-4a8e-11ed-bd51-0242ac120002",
    "address": {
      "street": "Rua Capitão João Paredes",
      "zip_code": "58046-710",
      "number": 234,
      "city": "João Pessoa",
      "state": "Paraíba",
      "is_delivery": True,
      "complement": "null"
    },
    "paid": True,
    "total_price": 679.95,
    "total_quantity": 10,
    "items": [
      {
        "product": {
          "code": 1,
          "name": "Barbie",
          "description": "Boneca de plástico",
          "price": 75,
          "stock": 50,
          "inmetro": "CE-BRI/ICEPEX-N 01264-25",
          "age_group": "null",
          "brand": "null",
          "material": "null",
          "height_dimension": "null",
          "width_dimension": "null",
          "length_dimension": "null",
          "image": "barbie.jpg",
          "guarantee": "null",
          "cor": "null",
          "topic": "null",
          "cartoon_character": "null",
          "best_uses": "null",
          "created_at": "2022-10-12T23:00:23.982000",
          "updated_at": "2022-10-12T23:00:23.982000"
        },
        "quantity": 5
      },
      {
        "product": {
          "code": 2,
          "name": "Uno",
          "description": "Jogo de cartas",
          "price": 60.99,
          "stock": 30,
          "inmetro": "CE-BRI/ICEPEX-N 01264-25",
          "age_group": "Maior de 10 anos",
          "brand": "Uno",
          "material": "papel",
          "height_dimension": 1,
          "width_dimension": 1,
          "length_dimension": 1,
          "image": "uno.jpg",
          "guarantee": "null",
          "cor": "Multicor",
          "topic": "Jogos de cartas",
          "cartoon_character": "null",
          "best_uses": "null",
          "created_at": "2022-10-12T23:00:23.982000",
          "updated_at": "2022-10-12T23:00:23.982000"
        },
        "quantity": 5
      }
    ],
    "created_at": "2022-10-13T00:33:39.929000",
    "updated_at": "2022-10-13T00:33:39.929000"
  }
    mock_get_order_by_id.return_value ={"order_id": "order_id"}
   
 
    respost = client_authenticated.post(f"/orders/?email=liviatestefinal%40gmail.com")
    assert respost.status_code == status.HTTP_201_CREATED




