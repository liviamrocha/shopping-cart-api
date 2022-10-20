import pytest
from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from unittest.mock import patch
from main import app
from shopping_cart.controllers import address
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
@patch("shopping_cart.cruds.address.find_user")
@patch("shopping_cart.cruds.address.find_address")
@patch("shopping_cart.cruds.address.delete_address")
@patch("shopping_cart.cruds.address.update_delivered_automatically")
def test_remove_address(mock_user,mock_find_user,mock_find_address,mock_delete,mock_deli_auto,client_authenticated):
  mock_user.return_value = {
       "email": "aaaaa@example.com"
  
  }
  mock_find_user.return_value = {"email": "aaaaa@example.com"}
  mock_find_address.return_value = {
    "email": "aaaaa@example.com",
     "street": "string",
    "zip_code": "string",
    "number": 0,
    "city": "string",
    "state": "string",
    "is_delivery": True,
    "complement": "string"
  }
  mock_delete.return_value = {
    "email": "aaaaa@example.com",
     "street": "string",
    "zip_code": "string",
    "number": 0,
    "city": "string",
    "state": "string",
    "is_delivery": True,
    "complement": "string"
  }
  mock_deli_auto.return_value = {
    "user.email": "email",

        "address.0.is_delivery" : True
  }
  address = {
  "street": "string",
  "zip_code": "string",
  "number": 0,
  "city": "string",
  "state": "string",
  "is_delivery": True,
  "complement": "string"
  }
  respost = client_authenticated.delete("/address/?email=pam%40pam.com", json = address)
  assert respost.status_code == status.HTTP_200_OK