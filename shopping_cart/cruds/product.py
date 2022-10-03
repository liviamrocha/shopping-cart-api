from shopping_cart.schemas.product import ProductSchema
from shopping_cart.server.database import db


# Criar um produto
async def create_product(product: ProductSchema):
    try:
        # Verifica se o produto já existe
        product_code = await db.product_db.find_one({"code": product.code})
        if product_code:
            return {"message": "Produto já cadastrado"}
        
        # Cria um novo produto
        product_db = await db.product_db.insert_one(product.dict())
        
        # Valida o cadastro e retorna a mensagem
        if product_db.inserted_id:
            return {"message": "Produto cadastrado"}
                
    # Retona a mensagem de erro
    except Exception as e:
            print(f'create_product.error: {e}')

            