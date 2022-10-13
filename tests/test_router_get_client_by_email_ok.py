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
def test_router_get_client_by_email_ok(mock_user_email):
  mock_user_email.return_value = {"name": "usuariah",
  "email": "aaaaa@example.com",
  "password": "string",
  "is_active": True,
  "is_admin": False,
  "created_at": "2022-10-05T20:37:30.682501"}
  respost = client.get(f"user/email?email=pam%40pam.com")
  assert respost.status_code == status.HTTP_200_OK