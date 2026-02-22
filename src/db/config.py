import os
from typing import Any

from dotenv import load_dotenv
from langchain_postgres import PGVector
from loguru import logger

load_dotenv()


class DatabaseConfig:
    """Classe de configuração para conexão com banco de dados PostgreSQL."""

    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL")
        self.collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_collection")
        self.embedding_model = os.getenv(
            "GOOGLE_EMBEDDING_MODEL", "text-embedding-004"
        )

        self._validate_config()

    def _validate_config(self) -> None:
        """Valida configurações obrigatórias do banco de dados."""
        if not self.database_url:
            logger.error("DATABASE_URL não configurado no arquivo .env")
            raise ValueError("DATABASE_URL é obrigatório")

        logger.info(f"Configuração do banco validada: {self.collection_name}")

    def get_vector_store(self, embeddings: Any) -> PGVector:
        """
        Cria e retorna uma instância do PGVector.

        Args:
            embeddings: Instância do modelo de embeddings

        Returns:
            Instância configurada do PGVector
        """
        try:
            logger.debug("Criando conexão com PGVector")
            vector_store = PGVector(
                embeddings=embeddings,
                collection_name=self.collection_name,
                connection=self.database_url,
                use_jsonb=True,
            )
            logger.success("PGVector configurado com sucesso")
            return vector_store
        except Exception as e:
            logger.error(f"Erro ao configurar PGVector: {e}")
            raise


# Instância global de configuração
db_config = DatabaseConfig()
