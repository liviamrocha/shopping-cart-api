from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
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
@patch("shopping_cart.cruds.cart.find_cart_by_email")
def test_router_get_by_email(mock_user_by_email, mock_find_cart_by_email, client_authenticated):
    mock_user_by_email.return_value = {"email": "email"}
    mock_find_cart_by_email.return_value = ExternalAPI(200)

    respost = client_authenticated.get(f"/carts/?email=pam%40pam.com")
    assert respost.status_code == status.HTTP_201_CREATED