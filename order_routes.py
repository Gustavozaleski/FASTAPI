from fastapi import APIRouter, Depends, HTTPException
from dependencies import criar_sessao, verificar_token
from schemas import pedidoschema
from sqlalchemy.orm import Session
from models import pedido, usuario


order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies= [Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você acessou a rota pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: pedidoschema , session: Session =  Depends(criar_sessao)):
    novo_pedido = pedido(usuario=pedido_schema.id)
    session.add(novo_pedido)
    session.commit()
    raise HTTPException(status_code=200, detail="Pedido efetuado com sucesso")

@order_router.post("pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    #se usario_encontrado.admin == true or usuario_encontrado.id === id_pedido

    pedido_cancelar = session.query(pedido).filter(pedido.id == id_pedido).first()
    if not pedido_cancelar:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    elif usuario_encontrado.admin == True or usuario_encontrado.id == pedido.usuario:
        pedido_cancelar.status = "CANCELADO"
        session.commit()
        return {
            "Mensagem": f"pedido nº {id_pedido} cancelado com sucesso",
            #"pedido": pedidos
            }

    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado para cancelar este pedido")

