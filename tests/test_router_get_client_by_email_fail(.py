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


@patch("shopping_cart.cruds.user.get_user_by_email")
def test_router_get_client_by_email_fail(mock_user_email,client_authenticated):
  mock_user_email.return_value = {}
  email = {"email":""}
  respost = client_authenticated.get(f"/user/email?email={email}",params=email)
  assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY




