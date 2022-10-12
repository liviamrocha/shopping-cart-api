from fastapi import APIRouter

# Minha API da rota principal
router = APIRouter(
    prefix="",
)


@router.get(
    "/",
    response_model=str,
)
async def index():
    return "Seja bem-vindo(a) ao Pytoys!"