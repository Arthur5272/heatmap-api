# Dengue Heatmap API

API em FastAPI para gerar e servir mapas coropléticos com incidência de casos de dengue em Pernambuco (PE), com a possibilidade de expansão para todo o Brasil.

## Funcionalidades

- **Endpoints REST**: Fornece dados agregados de casos de dengue por município.
- **Mapa Coroplético**: Gera um mapa HTML interativo (usando Folium) que visualiza a incidência de dengue.
- **Atualização Automática**: Um scheduler atualiza os dados periodicamente a partir do SINAN (via pySUS).
- **Segurança**: Endpoint administrativo protegido por chave de API para forçar a atualização dos dados.

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- Poetry

## Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd heatmap-api
   ```

2. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto, baseado no exemplo a seguir:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres_db:5432/dengue_db
   SYNC_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/dengue_db
   PYTHON_ENV=development
   SCHEDULER_INTERVAL_HOURS=6
   PY_SUS_YEARS=2023,2024
   GEOJSON_SOURCE=https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geo1_br_municipios.json
   SECRET_API_KEY=sua-chave-secreta-aqui
   ```

3. **Instale as dependências:**
   ```bash
   poetry install
   ```

4. **Inicie os serviços com Docker Compose:**
   Este comando irá iniciar o banco de dados PostgreSQL.
   ```bash
   docker-compose up -d
   ```

5. **Aplique as migrações do banco de dados:**
   (Certifique-se de que o container do banco de dados esteja rodando)
   ```bash
   poetry run alembic upgrade head
   ```

6. **Inicie a aplicação FastAPI:**
   ```bash
   poetry run uvicorn src.app.main:app --reload
   ```

   A API estará disponível em `http://localhost:8000`.

## Endpoints da API

- **GET /health**: Verifica o status da aplicação.
- **GET /api/v1/map**: Retorna um mapa HTML.
  - Parâmetros: `state` (str), `year` (int), `palette` (str).
  - Exemplo: `curl "http://localhost:8000/api/v1/map?state=PE&year=2024"`
- **GET /api/v1/cases**: Retorna dados agregados de casos.
  - Parâmetros: `year` (int), `state` (str, opcional).
  - Exemplo: `curl "http://localhost:8000/api/v1/cases?year=2024&state=PE"`
- **GET /api/v1/geojson/municipios**: Retorna o GeoJSON para um estado.
  - Parâmetros: `state` (str).
  - Exemplo: `curl "http://localhost:8000/api/v1/geojson/municipios?state=PE"`
- **POST /api/v1/admin/refresh**: Força a atualização dos dados.
  - Requer o header `X-API-KEY`.
  - Exemplo: `curl -X POST "http://localhost:8000/api/v1/admin/refresh" -H "X-API-KEY: sua-chave-secreta-aqui"`

## Estrutura do Projeto
(Uma breve descrição da estrutura de diretórios, se desejar)
```
/src
  /app
    /core       # Configurações centrais, banco de dados, scheduler
    /domain     # Modelos, schemas e casos de uso (regras de negócio)
    /infra      # Implementações concretas: repositórios, serviços externos, etc.
    /presentation # Templates HTML
  /migrations   # Migrações de banco de dados (Alembic)
```
