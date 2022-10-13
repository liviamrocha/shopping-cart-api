from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.dependencies.user_deps import get_current_user
from main import app
from unittest.mock import patch
import pytest
from shopping_cart.controllers.user import UserService
client = TestClient(app)

# @pytest.fixture
# def client():
#     """
#     Return an API Client
#     """
#     app.dependency_overrides = {}
#     return TestClient(app)

@pytest.fixture
def client_authenticated():
    """
    Returns an API client which skips the authentication
    """
    def skip_auth():
        pass
    app.dependency_overrides[get_current_user] = skip_auth
    return TestClient(app)



 
# @patch("shopping_cart.cruds.user.get_all_users")
# def test_create_user(client_authenticated,fastapi_dep,mocker):
#     mocker.return_value = []
#     """
#     Verify a user can be created and retrieved
#     """
#     def skip_auth():
#         pass
#     with fastapi_dep(app).override({get_current_user: skip_auth}):
#        respost = client_authenticated.get("/")

#         # Assert creation
#     assert respost.status_code == client_authenticated

@patch("shopping_cart.cruds.user.get_all_users")
#Testando a rota de busca de todos os usuários
def test_router_get_all_clients(mocker,client_authenticated):
  mocker.return_value = []
  respost = client_authenticated.get("/user/")
  #caso a busca sej possível deve retornar o status 200 OK
  assert respost.status_code == 200

# def test_get_override_two_dep(fastapi_dep):
#     with fastapi_dep(app).override(
#         {
#             first_dep: "plain_override_object",
           
#         }
#     ):
#         response = client.get("/depends")
#         assert response.status_code == 200
#         assert response.json() == {
#             "first_dep": "plain_override_object",
#             "second_dep": {"another": "override"},
#         }