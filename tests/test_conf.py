from fastapi import status
from fastapi.testclient import TestClient
from shopping_cart.server.database import URI
from main import app


#testando rota principal
def test_router_general():
  client = TestClient(app)
  respost = client.get("/")
  #como nada foi mandado para a rota principal deve retornar 404 not found
  assert respost.status_code == status.HTTP_200_OK

