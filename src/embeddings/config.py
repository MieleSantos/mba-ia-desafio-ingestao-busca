import os
from typing import Any

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Constantes de configuração
DEFAULT_GOOGLE_MODEL = "gemini-embedding-001"
DEPRECATED_GOOGLE_MODEL = "embedding-001"
DEFAULT_OPENAI_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSION = 768


class GoogleEmbeddings:
    """
    Cliente de embeddings do Google Generative AI (Gemini).
    Compatível com a interface LangChain (embed_documents, embed_query).
    """

    def __init__(
        self,
        model: str,
        output_dimensionality: int = DEFAULT_EMBEDDING_DIMENSION,
        api_key: str | None = None,
    ) -> None:
        if not api_key:
            raise ValueError("GOOGLE_API_KEY é obrigatória para GoogleEmbeddings")
        self._model = model
        self._output_dimensionality = output_dimensionality
        self._api_key = api_key
        self._genai = self._configure_genai()

    def _configure_genai(self) -> Any:
        """Configura e retorna o cliente genai (import tardio para evitar carga desnecessária)."""
        import google.generativeai as genai

        genai.configure(api_key=self._api_key)
        return genai

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Gera embeddings para uma lista de textos (ex.: chunks para índice)."""
        return [
            self._genai.embed_content(
                model=self._model,
                content=text,
                task_type="retrieval_document",
                output_dimensionality=self._output_dimensionality,
            )["embedding"]
            for text in texts
        ]

    def embed_query(self, text: str) -> list[float]:
        """Gera embedding para uma única query (ex.: pergunta do usuário)."""
        return self._genai.embed_content(
            model=self._model,
            content=text,
            task_type="retrieval_query",
            output_dimensionality=self._output_dimensionality,
        )["embedding"]


class EmbeddingConfig:
    """Classe de configuração para modelos de embedding (Google ou OpenAI)."""

    def __init__(self) -> None:
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_model = self._resolve_google_model(
            os.getenv("GOOGLE_EMBEDDING_MODEL", DEFAULT_GOOGLE_MODEL)
        )
        self.openai_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL", DEFAULT_OPENAI_MODEL
        )
        self.embedding_dim = int(
            os.getenv("EMBEDDING_DIMENSION", str(DEFAULT_EMBEDDING_DIMENSION))
        )
        self._validate_config()

    def _resolve_google_model(self, value: str) -> str:
        """Substitui modelo descontinuado pelo suportado."""
        if value == DEPRECATED_GOOGLE_MODEL:
            logger.warning(
                "GOOGLE_EMBEDDING_MODEL=embedding-001 está descontinuado; "
                "usando gemini-embedding-001. Atualize seu .env."
            )
            return DEFAULT_GOOGLE_MODEL
        return value

    def _validate_config(self) -> None:
        """Valida configurações de API keys."""
        if not self.google_api_key and not self.openai_api_key:
            logger.error(
                "Nenhuma API key configurada (GOOGLE_API_KEY ou OPENAI_API_KEY)"
            )
            raise ValueError("Pelo menos uma API key é obrigatória")

        if self.google_api_key:
            logger.info("Usando embeddings do Google AI")
        else:
            logger.info("Usando embeddings da OpenAI")

    def get_embeddings(self) -> Any:
        """Retorna a instância de embeddings configurada (Google ou OpenAI)."""
        if self.google_api_key:
            logger.info(f"Usando embeddings do Google: {self.google_model}")
            return GoogleEmbeddings(
                model=self.google_model,
                output_dimensionality=self.embedding_dim,
                api_key=self.google_api_key,
            )
        logger.info(f"Usando embeddings da OpenAI: {self.openai_model}")
        return self._create_openai_embeddings()

    def _create_openai_embeddings(self) -> Any:
        """Import tardio para não carregar OpenAI quando o provedor for Google."""
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(
            model=self.openai_model,
            openai_api_key=self.openai_api_key,
        )


embedding_config = EmbeddingConfig()
