import os
from typing import Any, Dict, List

from langchain_community.document_loaders import PyMuPDFLoader


class PDFLoader:
    """Class to load and extract text from PDF files using PyMuPDFLoader."""

    def __init__(self, file_path: str):
        """
        Initialize PDF loader with file path.

        Args:
            file_path: Path to the PDF file
        """
        self.file_path = file_path
        self._validate_file()

    def _validate_file(self) -> None:
        """Validate if the PDF file exists and is readable."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"PDF file not found: {self.file_path}")

        if not self.file_path.lower().endswith(".pdf"):
            raise ValueError(f"File must be a PDF: {self.file_path}")

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Load documents using PyMuPDFLoader.

        Returns:
            List of document dictionaries with metadata
        """
        try:
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
            raise RuntimeError(f"Error reading PDF file: {str(e)}")

    def load_text(self) -> str:
        """
        Extract all text from the PDF file.

        Returns:
            Complete text content from the PDF
        """
        documents = self.load_documents()
        return "\n\n".join(doc["page_content"] for doc in documents)

    def load_pages(self) -> List[str]:
        """
        Extract text from each page separately.

        Returns:
            List of text content per page
        """
        documents = self.load_documents()
        return [doc["page_content"] for doc in documents]

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get PDF metadata information.

        Returns:
            Dictionary with PDF metadata
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
            raise RuntimeError(f"Error reading PDF metadata: {str(e)}")


def load_pdf(file_path: str) -> str:
    """
    Convenience function to load text from PDF.

    Args:
        file_path: Path to the PDF file

    Returns:
        Complete text content from the PDF
    """
    loader = PDFLoader(file_path)
    return loader.load_text()
