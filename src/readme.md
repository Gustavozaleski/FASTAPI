# 🍕 API Pizzaria

API REST para gerenciamento de pedidos de uma pizzaria, construída com **FastAPI**. Inclui cadastro de usuários, autenticação com **JWT** (access e refresh token), níveis de acesso (usuário comum e administrador) e controle de pedidos.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

> 🚧 **Projeto em desenvolvimento.** Ainda não está finalizado: rotas, modelos e regras de negócio podem mudar, e algumas funcionalidades (como os itens do pedido) ainda não foram implementadas. Veja o [Roadmap](#roadmap) para o que está planejado.

## Funcionalidades

- Cadastro de usuários com senha criptografada (bcrypt)
- Login com JWT: access token (curta duração) e refresh token (longa duração)
- Rotas protegidas por token (padrão OAuth2 Bearer)
- Níveis de acesso: usuário comum e administrador
- Criação e cancelamento de pedidos, com regra de permissão (dono do pedido ou admin)
- Limite de requisições por rota (rate limit)
- Documentação interativa gerada automaticamente (Swagger)

## Tecnologias

| Tecnologia | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework da API |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM |
| [Alembic](https://alembic.sqlalchemy.org/) | Migrações do banco |
| SQLite | Banco de dados local |
| [Pydantic](https://docs.pydantic.dev/) | Schemas e validação |
| Passlib (bcrypt) | Criptografia de senhas |
| python-jose | Criação e validação de tokens JWT |
| python-dotenv | Variáveis de ambiente |
| fastapi-limiter + Redis | Limite de requisições |

## Estrutura do projeto

```
.
├── alembic/              # Migrações do banco
├── alembic.ini
├── auth_routes.py        # Rotas de autenticação (/auth)
├── order_routes.py       # Rotas de pedidos (/pedidos)
├── models.py             # Modelos do banco (usuários, pedidos, itens)
├── schemas.py            # Schemas Pydantic (entrada e saída)
├── dependencies.py       # Dependências (sessão do banco, verificação de token)
├── security.py           # bcrypt e esquema OAuth2
├── Config.py             # Leitura das variáveis do .env
├── main.py               # Criação do app e registro das rotas
├── requirements.txt
└── .env                  # Variáveis de ambiente (não versionado)
```

## Como rodar

### Pré-requisitos

- Python 3.13 (ou compatível com as versões do `requirements.txt`)
- Redis em execução, usado pelo rate limit (pode ser via Docker: `docker run -p 6379:6379 redis`)

### Instalação

```bash
# 1. Clone o repositório
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30
REFRESH_TOKEN_EXPIRE=7
RATELIMITER_TIME=5
RATELIMITER_SECONDS=60
```

| Variável | Descrição |
|---|---|
| `SECRET_KEY` | Chave usada para assinar os tokens JWT |
| `ALGORITHM` | Algoritmo do JWT (`HS256`) |
| `ACCESS_TOKEN_EXPIRE` | Duração do access token, em **minutos** |
| `REFRESH_TOKEN_EXPIRE` | Duração do refresh token, em **dias** |
| `RATELIMITER_TIME` | Número de requisições permitidas por janela |
| `RATELIMITER_SECONDS` | Tamanho da janela, em segundos |

Para gerar uma `SECRET_KEY` segura:

```bash
openssl rand -hex 32
```

> ⚠️ Nunca suba o `.env` para o Git.

### Banco de dados

Aplique as migrações para criar as tabelas:

```bash
alembic upgrade head
```

Sempre que alterar a estrutura dos modelos em `models.py`, gere uma nova migração:

```bash
alembic revision --autogenerate -m "descrição da alteração"
alembic upgrade head
```

### Iniciar o servidor

```bash
uvicorn main:app --reload
```

- API: http://127.0.0.1:8000
- Documentação (Swagger): http://127.0.0.1:8000/docs

## Endpoints

### Autenticação (`/auth`)

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| GET | `/auth/` | Rota padrão de autenticação (com rate limit) | Não |
| POST | `/auth/criar_conta` | Cadastra um novo usuário | Não |
| POST | `/auth/login` | Login com JSON; retorna access e refresh token | Não |
| POST | `/auth/login/test` | Login por formulário (botão **Authorize** do Swagger); retorna só o access token | Não |
| GET | `/auth/refresh` | Gera um novo access token | Sim |

### Pedidos (`/pedidos`)

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| GET | `/pedidos/` | Rota padrão de pedidos | Sim |
| POST | `/pedidos/pedido` | Cria um pedido | Sim |
| POST | `/pedidos/pedido/cancelar/{id_pedido}` | Cancela um pedido (dono do pedido ou admin) | Sim |

## Exemplos de uso

### Criar conta

```http
POST /auth/criar_conta
Content-Type: application/json

{
  "nome": "Maria",
  "email": "maria@email.com",
  "senha": "123456"
}
```

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "maria@email.com",
  "senha": "123456"
}
```

Resposta:

```json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "Bearer"
}
```

### Acessar uma rota protegida

Envie o access token no header `Authorization`:

```http
POST /pedidos/pedido/cancelar/1
Authorization: Bearer eyJhbGciOi...
```

### Renovar o access token

Envie o **refresh token** no header:

```http
GET /auth/refresh
Authorization: Bearer <refresh_token>
```

## Autenticação e níveis de acesso

1. O usuário faz login com e-mail e senha e recebe dois tokens.
2. O **access token** (curta duração) é enviado em toda requisição protegida: `Authorization: Bearer <token>`.
3. Quando o access token expira, o **refresh token** (longa duração) gera um novo access token em `/auth/refresh`.
4. Em cada requisição, o usuário é buscado no banco pelo id do token. O campo `admin` é sempre lido do banco, nunca confiado ao token.

| Código | Significado |
|---|---|
| 401 | Não autenticado (token ausente, inválido ou expirado) |
| 403 | Autenticado, mas sem permissão para a ação |

**Administradores** não são criados pelo cadastro público. O primeiro admin deve ser definido diretamente no banco (campo `admin = 1`) ou por um script de uso único.

## Modelo de dados

**usuarios**

| Campo | Tipo | Observação |
|---|---|---|
| id | Integer | Chave primária |
| nome | String | |
| email | String | Obrigatório |
| senha | String | Hash bcrypt |
| ativo | Boolean | Padrão: `True` |
| admin | Boolean | Padrão: `False` |

**Pedidos**

| Campo | Tipo | Observação |
|---|---|---|
| id | Integer | Chave primária |
| status | String | `PENDENTE`, `EM PREPARO`, `FINALIZADO`, `CANCELADO` |
| usuario | Integer | Chave estrangeira para `usuarios.id` |
| preco | Float | |

**Itens**

| Campo | Tipo | Observação |
|---|---|---|
| id | Integer | Chave primária |
| quantidade | Integer | |
| sabor | String | |
| tamanho | String | `PEQUENO`, `BROTO`, `MEDIO`, `GRANDE`, `FAMILIA`, `GRANDE-FAMILIA` |
| preco_unitario | Float | |
| pedidos | Integer | Chave estrangeira para `Pedidos.id` |


## Licença

Projeto de estudo, sem licença definida.
