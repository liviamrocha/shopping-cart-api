import pytest
from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from main import app
from unittest.mock import patch
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


@patch("shopping_cart.cruds.product.remove_product")
def test_router_delete_product_fail(mock_delete,client_authenticated):
  mock_delete.return_value = 1
  respost = client_authenticated.delete("/products/dois")
  assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY