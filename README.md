# 🍕 API de Pizzaria

API REST para gerenciamento de uma pizzaria, desenvolvida com Python e FastAPI. O projeto está em desenvolvimento, com foco na construção do backend, containerização, disponibilização em nuvem e futura integração com uma interface frontend desenvolvida em Flutter.

## 📌 Sobre o projeto

Este projeto consiste no desenvolvimento de uma API para uma pizzaria, com o objetivo de estruturar os principais recursos de um sistema de pedidos, gerenciamento de produtos e clientes.

A aplicação está sendo desenvolvida utilizando boas práticas de organização de código, gerenciamento de dependências e containerização, visando facilitar sua manutenção, escalabilidade e futura integração com uma aplicação frontend.

## 🚧 Status do projeto

**Em desenvolvimento**

- [x] Estrutura inicial da aplicação FastAPI
- [x] Organização do projeto utilizando `src`
- [x] Gerenciamento de dependências com `uv`
- [x] Configuração do Dockerfile
- [x] Configuração do Docker Compose
- [ ] Implementação dos endpoints
- [ ] Integração com banco de dados PostgreSQL
- [ ] Migrações com Alembic
- [ ] Deploy da API na nuvem
- [ ] Desenvolvimento da interface em Flutter
- [ ] Integração entre frontend e backend

## 🛠️ Tecnologias utilizadas

| Tecnologia | Descrição |
|---|---|
| Python | Linguagem utilizada no desenvolvimento do backend |
| FastAPI | Framework para construção da API REST |
| uv | Gerenciamento de dependências e ambiente Python |
| Docker | Containerização da aplicação |
| Docker Compose | Gerenciamento dos serviços e ambiente de execução |
| PostgreSQL | Banco de dados relacional |
| Alembic | Gerenciamento de migrações do banco de dados |
| Flutter | Tecnologia planejada para o desenvolvimento do frontend |

## 🏗️ Estrutura do projeto

```text
.
├── alembic/             # Migrações do banco de dados
├── database/             # Arquivos relacionados ao banco
├── src/                  # Código-fonte da aplicação
│   └── my_package/       # Pacote principal
├── tests/                # Testes automatizados
├── Dockerfile            # Configuração da imagem Docker
├── docker-compose.yml     # Configuração dos serviços
├── pyproject.toml        # Configurações e dependências do projeto
├── uv.lock              # Lockfile de dependências
└── .dockerignore         # Arquivos excluídos do contexto Docker
```

## 🐳 Executando o projeto

### Pré-requisitos

- Python
- Docker
- Docker Compose
- Git

### Clonando o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```

### Executando com Docker Compose

Para construir a imagem e iniciar os serviços:

```bash
docker compose up --build
```

Para executar os containers em segundo plano:

```bash
docker compose up --build -d
```

Para parar os serviços:

```bash
docker compose down
```

## 📚 Documentação da API

A documentação interativa é gerada automaticamente pelo FastAPI.

Com a aplicação em execução, acesse:

- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

Por meio dessas interfaces, é possível visualizar os endpoints, seus parâmetros, os modelos de dados e testar as requisições diretamente.

## ☁️ Deploy e arquitetura planejada

O backend está sendo preparado para disponibilização em nuvem, utilizando Docker para padronizar o ambiente de execução e facilitar o processo de implantação.

A arquitetura planejada prevê a separação entre backend e frontend:

- **Backend:** API REST desenvolvida com FastAPI.
- **Frontend:** Aplicação mobile desenvolvida com Flutter.
- **Banco de dados:** PostgreSQL.
- **Infraestrutura:** Aplicação containerizada e hospedada na nuvem.

## 🗺️ Roadmap

- [ ] Estruturar e desenvolver os endpoints da API
- [ ] Implementar gerenciamento de produtos e cardápio
- [ ] Implementar gerenciamento de clientes
- [ ] Desenvolver sistema de pedidos
- [ ] Implementar autenticação e autorização
- [ ] Configurar banco de dados PostgreSQL
- [ ] Implementar migrações com Alembic
- [ ] Disponibilizar API na nuvem
- [ ] Desenvolver interface mobile com Flutter
- [ ] Integrar Flutter com a API

## 👨‍💻 Autor

Projeto desenvolvido para aprimorar conhecimentos em desenvolvimento backend, construção de APIs REST, arquitetura de software, containerização, banco de dados e deploy em nuvem.
