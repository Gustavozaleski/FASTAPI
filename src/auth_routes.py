from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from Config import (
    ACCESS_TOKEN_EXPIRE,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE,
    SECRET_KEY,
)
from dependencies import criar_sessao, verificar_token
from models import usuario
from schemas import LoginSchema, Usuarioschema
from security import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def criar_token(
    id_usuario, email, duracao_token=timedelta(minutes=int(ACCESS_TOKEN_EXPIRE))
):
    data_expiracao = datetime.now(UTC) + duracao_token
    dic_info = {"sub": str(id_usuario), "user_email": email, "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario_buscado = session.query(usuario).filter(usuario.email == email).first()
    if not usuario_buscado or not bcrypt_context.verify(senha, usuario_buscado.senha):
        return False

    return usuario_buscado


@auth_router.get("/")
async def home():
    return {"Mensagem": "voce acessou a rota padrão de autenticação"}


@auth_router.post("/Criar_conta")
async def criar_conta(Usuario_schema: Usuarioschema, session=Depends(criar_sessao)):
    usuario_sistema = (
        session.query(usuario).filter(Usuario_schema.email == usuario.email).first()
    )
    if usuario_sistema:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado")
    senha_cripografada = bcrypt_context.hash(Usuario_schema.senha)
    novo_usuario = usuario(
        Usuario_schema.nome,
        Usuario_schema.email,
        senha_cripografada,
        Usuario_schema.ativo,
        Usuario_schema.admin,
    )
    session.add(novo_usuario)
    session.commit()
    raise HTTPException(
        status_code=200, detail=f"Email cadastrado com sucesso {novo_usuario.email}"
    )


@auth_router.post("/login")
async def login(Login_schema: LoginSchema, session: Session = Depends(criar_sessao)):
    usuario_login = autenticar_usuario(Login_schema.email, Login_schema.senha, session)
    if not usuario_login:
        raise HTTPException(
            status_code=400, detail="Usuario não encontrado ou senha incorreta"
        )
    acess_token = criar_token(usuario_login.id, usuario_login.email)
    refresh_token = criar_token(
        usuario_login.id, usuario_login.email, timedelta(days=REFRESH_TOKEN_EXPIRE)
    )
    return {
        "access_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@auth_router.post("/login/test")
async def login_test(
    dados_formulario: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(criar_sessao),
):
    usuario_login = autenticar_usuario(
        dados_formulario.username, dados_formulario.password, session
    )
    if not usuario_login:
        raise HTTPException(
            status_code=400, detail="Usuario não encontrado ou senha incorreta"
        )
    acess_token = criar_token(usuario_login.id, usuario_login.email)
    refresh_token = criar_token(
        usuario_login.id, usuario_login.email, timedelta(days=REFRESH_TOKEN_EXPIRE)
    )
    return {"access_token": acess_token, "token_type": "Bearer"}


@auth_router.get("/refresh")
async def use_refresh_token(
    usuario_encontrado: usuario = Depends(verificar_token),
    session=Depends(criar_sessao),
):
    access_token = criar_token(usuario_encontrado.id, usuario_encontrado.email)
    return {"access_token": access_token, "token_type": "Bearer"}
