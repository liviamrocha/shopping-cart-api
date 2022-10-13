import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


@patch("shopping_cart.cruds.product.list_products")
def test_router_get_products(mock_get):
    mock_get.return_value = []
    respost = client.get("/products/")
    assert respost.status_code == status.HTTP_200_OK