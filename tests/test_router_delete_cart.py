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

class ExternalAPI():
  def __init__(self,status_code,response=None):
    self.status_code = status_code
    self.response = response
  def json(self):
    return self.response
client = TestClient(app)

@patch("shopping_cart.cruds.cart.get_user_cart")
@patch("shopping_cart.cruds.cart.check_cart_item")
@patch("shopping_cart.controllers.cart.validate_quantity_to_remove")
@patch("shopping_cart.cruds.product.product_by_id")
@patch("shopping_cart.controllers.cart.validate_product")
def test_router_get_order_by_id(mock_get_user_cart,mock_check_cart_item,mock_validate_quantity_to_remove,
                                mock_product_by_id,mock_validate_product,client_authenticated):
    mock_get_user_cart.return_value = {"user.email": "email"}
    mock_check_cart_item.return_value =  {"user.email": "email", 
    "order_items.product.code": "product_id"}
    mock_validate_quantity_to_remove.return_value = ExternalAPI(201)
    mock_product_by_id.return_value = {"code": "code"}  
    mock_validate_product.return_value = None
    
    bory = {
  "product_id": 1,
  "quantity": 1
}
    respost = client_authenticated.delete(f"/carts/?email=liviatestefinal%40gmail.com")
    assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


