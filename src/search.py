from db.config import db_config
from embeddings.config import embedding_config
from loguru import logger

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def vector_search(question: str):
    """Realiza uma busca vetorial para encontrar os chunks mais relevantes."""
    # Configurar embeddings e vector store
    embeddings = embedding_config.get_embeddings()
    vector_store = db_config.get_vector_store(embeddings)

    # Realizar a busca vetorial
    results = vector_store.similarity_search_with_score(query=question, k=10)
    logger.info(f"Resultados da busca vetorial: {len(results)}")

    filtered_docs = [doc for doc, score in results]
    contexto = "\n\n".join([doc.page_content for doc in filtered_docs])

    # Debug: confirme que o contexto está sendo montado (e se faz sentido reingerir ao trocar de modelo)
    # logger.info(f"Contexto enviado ao LLM: {len(contexto)} caracteres")
    # if contexto.strip():
    #     logger.debug(f"Preview do contexto: {contexto.strip()[:400]}...")
    # else:
    #     logger.warning(
    #         "Contexto vazio. Se você trocou o modelo de embedding, reexecute a ingestão (ingest)."
    #     )

    return contexto


def search_prompt(question=None):
    contexto = vector_search(question)
    return PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)
