# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de **RAG (Retrieval Augmented Generation)** para ingestão e busca em documentos PDF: geração de chunks, armazenamento vetorial e chat com o usuário com base no conteúdo ingerido.

## Tecnologias

| Área | Tecnologia |
|------|------------|
| **Linguagem** | Python 3.10+ |
| **Gerenciamento de dependências** | Poetry |
| **Orquestração de LLM e RAG** | LangChain |
| **Embeddings** | Google Generative AI (Gemini) ou OpenAI |
| **Banco vetorial** | PostgreSQL + pgvector (LangChain PGVector) |
| **Banco de dados** | Docker / Docker Compose (PostgreSQL 17 + pgvector) |
| **Carregamento de PDF** | PyMuPDF (langchain-community) |
| **Chat** | LangChain + Google Gemini (gemini-2.5-flash-lite) |

## Requisitos

- Python 3.10+
- Docker e Docker Compose
- API Key do Google (Gemini) ou OpenAI (para embeddings e, no chat, Gemini)

## Configuração

1. Clone o repositório e instale as dependências com Poetry:

```bash
poetry install
```

2. Copie o arquivo de exemplo e configure o `.env`:

```bash
cp .env.example .env
```

3. Edite o `.env` com suas chaves e caminhos:

```env
# Embeddings (use um dos dois)
GOOGLE_API_KEY=sua_chave_google
GOOGLE_EMBEDDING_MODEL=gemini-embedding-001

# Opcional: OpenAI como alternativa aos embeddings
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Banco (conexão do Docker Compose)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=rag_collection

# Caminho do PDF a ser ingerido
PDF_PATH=database/document.pdf
```

## Como rodar o projeto

### 1. Subir o banco de dados (PostgreSQL + pgvector)

```bash
docker compose up -d
```

Isso sobe o PostgreSQL 17 com a extensão pgvector. Um job de bootstrap cria a extensão `vector` no banco `rag`.

### 2. Gerar os chunks e popular o banco vetorial

Com o PDF em `PDF_PATH` (ex.: `database/document.pdf`), rode a ingestão:

```bash
poetry run python -m src.ingest
```

Ou, ativando o ambiente do Poetry:

```bash
poetry shell
 python src/ingest.py
```

O script `ingest.py` carrega o PDF, quebra em chunks, gera embeddings e grava no PGVector.

### 3. Chat com o usuário

```bash
poetry run python -m src.chat
```

Ou, dentro do `poetry shell`:

```bash
 python src/chat.py
```

O `chat.py` lê uma pergunta do usuário, busca os trechos relevantes no banco vetorial e envia contexto + pergunta ao modelo (Gemini) para responder com base no documento.

## Ordem resumida

```text
1. docker compose up -d          # sobe o banco
2. python src/ingest.py         # gera chunks e embeddings
3. python src/ingest.py          # chat com o usuário
```

## Estrutura do projeto

```text
.
├── src/
│   ├── chat.py           # Chat com o usuário (pergunta → busca vetorial → resposta)
│   ├── ingest.py         # Ingestão do PDF: gera chunks e salva no PGVector
│   ├── search.py         # Busca vetorial e montagem do prompt RAG
│   ├── pdf_loader.py     # Carregamento de PDFs (PyMuPDF)
│   ├── embeddings/       # Configuração de embeddings (Google/OpenAI)
│   │   └── config.py
│   └── db/               # Configuração do banco (PGVector)
│       └── config.py
├── database/             # Coloque aqui o(s) PDF(s) para ingestão
├── docker-compose.yml    # PostgreSQL + pgvector
├── pyproject.toml       # Dependências (Poetry)
└── .env                 # Variáveis de ambiente (não versionado)
```

## Documentação

A documentação é gerada com **MkDocs** (tema Material) e **mkdocstrings** (API a partir dos docstrings).

```bash
# Instalar dependências de desenvolvimento (inclui mkdocs)
poetry install

# Servir a documentação localmente (http://127.0.0.1:8000)
poetry run mkdocs serve

# Gerar o site estático em site/
poetry run mkdocs build
```

## Observações

- **Embedding dimension**: o default é 768 (`EMBEDDING_DIMENSION=768`). Se alterar o modelo ou a dimensão, pode ser necessário reingerir o PDF para manter consistência no banco.
- **Modelo de embedding**: use `gemini-embedding-001`; o modelo antigo `embedding-001` foi descontinuado.
