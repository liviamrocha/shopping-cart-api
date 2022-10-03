from pydantic import BaseModel, Field


# Modelo base de um produto (para cadastro)
class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    material: str
    inmetro: str
    code: str = Field(unique=True)
    stock: int

# Modelo de retorno de um documento de produto
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "material": product["material"],
        "inmetro": product["inmetro"],
        "code": product["code"],
        "stock": product["stock"],
    }
    

