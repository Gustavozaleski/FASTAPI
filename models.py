from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey 
from sqlalchemy.orm import declarative_base
#from sqlalchemy_utils.types import ChoiceType 

#Criação de conexão com o banco de dados
db = create_engine("sqlite:///banco.db")

#Criação da base do banco de dados
Base = declarative_base()

#criação das classes/tabelas no banco de dados

#usuarios
class usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#pedido
class pedido(Base):
    __tablename__ = "Pedidos"

    """STATUS_PEDIDOS = {("PENDENTE","PENDENTE"),
                      ("CANCELADO", "CANCELADO"),
                      ("FINALIZADO", "FINALIZADO"),
                      ("EM PREPARO", "EM PREPARO")}"""

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float , nullable=False)
    # itens = 

    def __init__(self,usuario, status="Pendente", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
        


#itenspedidos
class itenspedido(Base):
    __tablename__ = "Itens"

    """TAMANHOS = {("PEQUENO", "PEQUENO"),
                ("BROTO","BROTO"),
                ("MEDIO","MEDIO"),
                ("GRANDE","GRANDE"),
                ("FAMILIA","FAMILIA"),
                ("GRANDE-FAMILIA","GRANDE-FAMILIA")}"""

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("Quantidade", Integer, nullable=False)
    sabor = Column("Sabor", String)
    tamanho = Column("Tamanho", String, nullable=False)
    preco_unitario = Column("Preco unitario", Float, nullable=False)
    pedidos = Column("pedidos", ForeignKey("Pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedidos):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedidos = pedidos


#Executa a criação dos metadados do seu banco (cria o banco de dados)