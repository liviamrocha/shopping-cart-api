from fastapi import APIRouter

router = APIRouter(
    prefix="",
)

@router.get(
    "/",
    response_model=str,
    include_in_schema=False
)
async def index():
    return "Seja bem-vindo(a) ao Pytoys!"