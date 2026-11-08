from pydantic import BaseModel, ConfigDict
from typing import Optional

class Usuarioschema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False


    model_config = ConfigDict(from_attributes=True)
    

class pedidoschema(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: str
    senha: str

    model_config = ConfigDict(from_attributes=True)

class ItensSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    model_config = ConfigDict(from_attributes=True)
   