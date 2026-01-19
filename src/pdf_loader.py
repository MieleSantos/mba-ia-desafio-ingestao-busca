import os
from typing import Any, Dict, List

from langchain_community.document_loaders import PyMuPDFLoader
from loguru import logger


class PDFLoader:
    """Classe para carregar e extrair texto de arquivos PDF usando PyMuPDFLoader."""

    def __init__(self, file_path: str):
        """
        Inicializa o carregador PDF com o caminho do arquivo.

        Args:
            file_path: Caminho para o arquivo PDF
        """
        self.file_path = file_path
        self._validate_file()

    def _validate_file(self) -> None:
        """Valida se o arquivo PDF existe e é legível."""
        if not os.path.exists(self.file_path):
            logger.error(f"Arquivo PDF não encontrado: {self.file_path}")
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")

        if not self.file_path.lower().endswith(".pdf"):
            logger.error(f"Arquivo deve ser um PDF: {self.file_path}")
            raise ValueError(f"File must be a PDF: {self.file_path}")

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Carrega documentos usando PyMuPDFLoader.

        Returns:
            Lista de dicionários de documentos com metadados
        """
        try:
            logger.debug(f"Carregando documentos do PDF: {self.file_path}")
            loader = PyMuPDFLoader(self.file_path)
            documents = loader.load()

            # Convert to list of dictionaries for easier processing
            result = []
            for doc in documents:
                result.append(
                    {
                        "page_content": doc.page_content,
                        "metadata": doc.metadata,
                        "type": "Document",
                    }
                )

            return result

        except Exception as e:
            logger.error(f"Erro ao ler arquivo PDF: {str(e)}")
            raise RuntimeError(f"Error reading PDF file: {str(e)}")

    def load_text(self) -> str:
        """
        Extrai todo o texto do arquivo PDF.

        Returns:
            Conteúdo de texto completo do PDF
        """
        documents = self.load_documents()
        return "\n\n".join(doc["page_content"] for doc in documents)

    def load_pages(self) -> List[str]:
        """
        Extrai texto de cada página separadamente.

        Returns:
            Lista de conteúdo de texto por página
        """
        documents = self.load_documents()
        return [doc["page_content"] for doc in documents]

    def get_metadata(self) -> Dict[str, Any]:
        """
        Obtém informações de metadados do PDF.

        Returns:
            Dicionário com metadados do PDF
        """
        try:
            loader = PyMuPDFLoader(self.file_path)
            documents = loader.load()

            if documents:
                metadata = {
                    "num_pages": len(documents),
                    "file_size": os.path.getsize(self.file_path),
                    "metadata": documents[0].metadata if documents else {},
                }
                return metadata
            else:
                return {
                    "num_pages": 0,
                    "file_size": os.path.getsize(self.file_path),
                    "metadata": {},
                }

        except Exception as e:
            logger.error(f"Erro ao ler metadados do PDF: {str(e)}")
            raise RuntimeError(f"Error reading PDF metadata: {str(e)}")


def load_pdf(file_path: str) -> str:
    """
    Função de conveniência para carregar texto de PDF.

    Args:
        file_path: Caminho para o arquivo PDF

    Returns:
        Conteúdo de texto completo do PDF
    """
    loader = PDFLoader(file_path)
    return loader.load_text()
