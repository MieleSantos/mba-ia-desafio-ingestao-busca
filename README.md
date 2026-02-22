# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de RAG (Retrieval Augmented Generation) para ingestion e busca em documentos PDF.

## Requisitos

- Python 3.10+
- Docker e Docker Compose
- PostgreSQL (via Docker)
- API Key do Google Gemini ou OpenAI

## Configuração

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Configure as variáveis de ambiente no arquivo `.env`:
```env
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_EMBEDDING_MODEL='text-embedding-004'
OPENAI_API_KEY=
OPENAI_EMBEDDING_MODEL='text-embedding-3-small'
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=rag_collection
PDF_PATH=database/document.pdf
```

## Orden de Execução

### 1. Subir o banco de dados:
```bash
docker compose up -d
```

### 2. Executar ingestão do PDF:
```bash
python src/ingest.py
```

### 3. Rodar o chat:
```bash
python src/chat.py
```

## Estrutura do Projeto

```
.
├── src/
│   ├── chat.py          # Interface de chat
│   ├── ingest.py        # Script de ingestão de PDF
│   ├── pdf_loader.py    # Carregador de PDFs
│   ├── search.py        # Módulo de busca
│   ├── embeddings/      # Configuração de embeddings
│   └── db/              # Configuração do banco de dados
├── database/
│   └── document.pdf     # PDF para ingestão
├── docker-compose.yml   # Configuração do PostgreSQL
└── .env                 # Variáveis de ambiente
```
