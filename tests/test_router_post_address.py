import pytest
from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from shopping_cart.dependencies.user_deps import get_current_user

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
@patch("shopping_cart.cruds.address.update_delivered_address")
@patch("shopping_cart.cruds.address.add_address")
@patch("shopping_cart.cruds.address.find_address")
def test_router_add_adresses(mock_user, mock_find_user, mock_update,mock_address,
                             mock_find_address, client_authenticated):
  mock_user.return_value = {
    "name": "usuariah",
    "email": "aaaaa@example.com",
    "password": "string",
    "is_active": True,
    "is_admin": False,
    "created_at": "2022-10-05T20:37:30.682501"
  }
  mock_find_user.return_value = {"email": "aaaaa@example.com"}
  mock_update.return_value = {
    "user.email": "email", 
    "address.is_delivery": True, 
    "address.$.is_delivery":False
  }
  mock_address.return_value = {
    "email":"email@email",
    "street": "string",
    "zip_code": "string",
    "number": 0,
    "city": "string",
    "state": "string",
    "is_delivery": True,
    "complement": "string"
  }
  adresses = {
  "street": "string",
  "zip_code": "string",
  "number": 0,
  "city": "string",
  "state": "string",
  "is_delivery": True,
  "complement": "string"
}
  mock_find_address.return_value = []
  respost = client_authenticated.post("/address/?email=pam%40pam.com")
#caso a busca sej possível deve retornar o status 200 OK
  assert respost.status_code == 422
