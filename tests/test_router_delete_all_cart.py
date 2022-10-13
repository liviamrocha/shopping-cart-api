from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
import pytest
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

@patch("shopping_cart.cruds.cart.get_user_cart")
@patch("shopping_cart.cruds.cart.check_cart_item")
@patch("shopping_cart.cruds.cart.delete_cart")
@patch("shopping_cart.cruds.user.get_user_by_email")

def test_router_delete_all_cart(mock_get_user_cart,mock_check_cart_item,mock_delete,mock_get_user_by_email
                                ,client_authenticated):
    mock_get_user_cart.return_value = {"user.email": "email"}
    mock_check_cart_item.return_value =  {"user.email": "email", 
    "order_items.product.code": "product_id"}
    mock_delete.return_value = {"user.email": "email"}
    mock_get_user_by_email.return_value = {"user.email": "email"}
  
    
    bory = {
  "product_id": 1,
  "quantity": 1
}
    respost = client_authenticated.delete(f"/carts/all?email=pam%40pam.com")
    assert respost.status_code == status.HTTP_202_ACCEPTED