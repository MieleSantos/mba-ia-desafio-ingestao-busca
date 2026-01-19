import os
from typing import Any

from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class EmbeddingConfig:
    """Classe de configuração para modelos de embedding."""

    def __init__(self) -> None:
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_model = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
        self.openai_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

        self._validate_config()

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
        """Retorna a instância de embeddings configurada."""
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from langchain_openai import OpenAIEmbeddings

        if self.google_api_key:
            logger.info(f"Usando embeddings do Google: {self.google_model}")
            return GoogleGenerativeAIEmbeddings(
                model=self.google_model,
                google_api_key=self.google_api_key,
            )
        else:
            logger.info(f"Usando embeddings da OpenAI: {self.openai_model}")
            return OpenAIEmbeddings(
                model=self.openai_model,
                openai_api_key=self.openai_api_key,
            )


# Instância global de configuração
embedding_config = EmbeddingConfig()
