from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from main import app
from unittest.mock import patch
import pytest
from shopping_cart.controllers.cart import fetch_cart_by_email

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


client = TestClient(app)
@patch("shopping_cart.cruds.user.get_user_by_email")
@patch("shopping_cart.cruds.product.product_by_id")
@patch("shopping_cart.cruds.cart.find_cart_by_email")

def test_router_create_cart_fail(mock_get_user_by_email,mock_product_by_id,mock_find_cart,client_authenticated):
    mock_get_user_by_email.return_value = {"email": "email"}
    mock_product_by_id.return_value = 1
    mock_find_cart.return_value = ExternalAPI(201)
    bory = {
  "product_id": 0,
  "quantity": 0
}
    respost = client_authenticated.post("/carts/?email=pam%40pam.com",json=bory)
#caso a busca sej possível deve retornar o status 200 OK
    assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

