import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)


def test_router_get_product_by_name_without_name():
  respost = client.get("/products/name")
  assert respost.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY