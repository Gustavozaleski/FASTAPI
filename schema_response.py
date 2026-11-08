from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from schemas import ItensSchema

class ResponsePedidoSchema(BaseModel):
    id: int 
    status: str
    preco: float


    model_config = ConfigDict(from_attributes=True)

