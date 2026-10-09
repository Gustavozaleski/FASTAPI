from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=["Auth"])

@auth_router.get("/")
async def autenticar():
    return {"Mensagem": "voce acessou a rota padrão de autenticação"}