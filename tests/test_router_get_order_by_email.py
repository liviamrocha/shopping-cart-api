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


def test_router_get_order_by_id(client_authenticated):

    bory = {
        "email":"email",
        "order_id" : "dfnjkvnvckjcv"
    }
    respost = client_authenticated.get(f"/orders/items?email=pam%40pam&order_id=213342ef%5Cv%5Cv")
    assert respost.status_code == 422