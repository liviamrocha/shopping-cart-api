from asyncio.windows_events import NULL
from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from main import app
from unittest.mock import patch
client = TestClient(app)

@patch("shopping_cart.cruds.user.get_user_by_email")
@patch("shopping_cart.cruds.order.find_user_order")
@patch("shopping_cart.cruds.order.get_orders_count")
def test_router_get_order_count(mock_get_user_by_email,mock_find_user_order,mock_get_orders_count ):
    mock_get_user_by_email.return_value = {"email": "email"}
    mock_find_user_order.return_value = {"user.email": "email"}
    mock_get_orders_count.retuen_value - {"user.email": "email"} 
    respost = client.get(f"/orders/count?email=liviatestefinal%40gmail.com")
    assert respost.status_code == status.HTTP_200_OK