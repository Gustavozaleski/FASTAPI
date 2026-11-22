from fastapi import APIRouter, Depends, HTTPException
from dependencies import criar_sessao, verificar_token
from schemas import pedidoschema, ItensSchema
from schema_response import ResponsePedidoSchema
from sqlalchemy.orm import Session
from models import pedido, usuario, itenspedido
from typing import List

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
            "Mensagem": f"pedido nº {pedido_cancelar.id} cancelado com sucesso",
            "pedido": pedido_cancelar
            }

    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado para cancelar este pedido")

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    if usuario_encontrado.admin == False:
        raise HTTPException(status_code=401, detail="Você não é autorizado para acessar essa operação")
    else:
        pedidos = session.query(pedido).all()
        return {
            "Pedidos": pedidos
        }

@order_router.post("pedido/adicionar-item/{id_pedido}")
async def adicionar_item(id_pedido: int, item: ItensSchema ,session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    Pedido = session.query(pedido).filter(pedido.id == id_pedido).first()
    if not Pedido:
        raise HTTPException(status_code=400, detail="Pedido não existe")
    elif usuario_encontrado.admin == True or usuario_encontrado.id == pedido.usuario:
        item_pedido = itenspedido(item.quantidade,item.sabor, item.tamanho, item.preco_unitario, id_pedido)
        session.add(item_pedido)
        Pedido.calcular_preco()
        session.commit()
        return {
            "mensagem": "Item criado com sucesso",
            "item_id": item_pedido.id,
            "preço_pedido": Pedido.preco
        }
    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")

@order_router.post("pedido/remover-item/{id_item_pedido}")
async def remover_item(id_item_pedido: int, session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    item_pedido = session.query(itenspedido).filter(itenspedido.id == id_item_pedido).first()
    Pedido  = session.query(pedido).filter(pedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="item no pedido não existente")
    elif usuario_encontrado.admin == True or usuario_encontrado.id == Pedido.usuario:
        session.delete(item_pedido)
        
        Pedido.calcular_preco()
        session.commit()
        return {
            "mensagem": f"Item  de número Nº{id_item_pedido} removido com sucesso",
            "itens_pedido": len(Pedido.itens),
            "pedido": Pedido
        }
    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")

@order_router.post("pedido/finalizar-pedido/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    #se usario_encontrado.admin == true or usuario_encontrado.id === id_pedido

    pedido_cancelar = session.query(pedido).filter(pedido.id == id_pedido).first()
    if not pedido_cancelar:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    elif usuario_encontrado.admin == True or usuario_encontrado.id == pedido.usuario:
        pedido_cancelar.status = "FINALIZADO"
        session.commit()
        return {
            "Mensagem": f"pedido nº {pedido_cancelar.id} finalizado com sucesso",
            "pedido": pedido_cancelar
            }

    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado para finalizar este pedido")

@order_router.get("pedido/visualizar/{id_pedido}", response_model=ResponsePedidoSchema)
async def visualizar_pedido(id_pedido: int, session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    pedido_visualizar = session.query(pedido).filter(pedido.id == id_pedido).first()
    if not pedido_visualizar:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    elif usuario_encontrado.admin == True or usuario_encontrado.id == pedido.usuario:
        
        
        return {
            "Mensagem": f"pedido nº {pedido_visualizar.id}",
            "pedido": pedido_visualizar,
            "quantidade": pedido_visualizar.itens
             }
    
    else:
        raise HTTPException(status_code=401, detail="Usuário não autorizado para visualizar este pedido")
    
@order_router.get("listar/pedidos/admin", response_model=List[ResponsePedidoSchema])
async def visualizar_todos(session: Session = Depends(criar_sessao), usuario_encontrado: usuario = Depends(verificar_token)):
    if not usuario_encontrado.admin:
        raise HTTPException(status_code=401, detail="Usuário não autorizado para visualizar todos os pedidos")
    else:
        Pedidos_usuario = session.query(pedido).all()
        return {
            "Pedidos": Pedidos_usuario
        }