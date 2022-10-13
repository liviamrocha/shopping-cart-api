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


#Testando o cadastro de um novo cliente
@patch("shopping_cart.controllers.user.validate_user")
@patch("shopping_cart.controllers.user.UserService.create_user_security")
def test_router_post_a_client_fail(mock_vali, mock_create,client_authenticated):
  mock_vali.return_value = {
  "name": "usuariah",
  "email": "aaaaa@example.com",
  "password": "string",
  "is_active": True,
  "is_admin": False,
  "created_at": "2022-10-05T20:37:30.682501"
}
  mock_create.return_value = None
  usuario = {
  "name": "usuariah",
  "email": "aaaaa@example.com",
  "password": "string",
  "is_active": True,
  "is_admin": False,
  "created_at": "2022-10-05T20:37:30.682501"
}
  respost = client_authenticated.post("/user/")
  assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
