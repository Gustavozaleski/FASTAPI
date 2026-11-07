from models import usuario, db
from models import usuario
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from schemas import Usuarioschema
from sqlalchemy.orm import sessionmaker
from jose import jwt,JWTError
from Config import SECRET_KEY, ALGORITHM
from security import oauth2_schema

def criar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str=Depends(oauth2_schema), session = Depends(criar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
      
        raise HTTPException(status_code=401, detail="Acesso negado")
    buscar_usuario = session.query(usuario).filter(usuario.id == id_usuario).first()
    if not buscar_usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return buscar_usuario
