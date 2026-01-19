import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from db.config import db_config
from embeddings.config import embedding_config
from pdf_loader import PDFLoader

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")


def text_split() -> RecursiveCharacterTextSplitter:
    """Configura o text splitter para dividir o texto em chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", " ", ""]
    )
    return text_splitter


def generate_chunks(
    text_splitter: RecursiveCharacterTextSplitter, documents: list[Document]
) -> list[Document]:
    """Gera chunks de texto a partir dos documentos fornecidos."""
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Total de chunks: {len(chunks)}")

    return chunks


def ingest_pdf() -> None:
    """Função principal de ingestão de PDF para o vector store."""
    if not PDF_PATH:
        logger.error("PDF_PATH não configurado no arquivo .env")
        return

    try:
        logger.info(f"Iniciando ingestão do PDF: {PDF_PATH}")
        pdf = PDFLoader(PDF_PATH)

        # Carregar e dividir documentos
        raw_documents = pdf.load_documents()
        logger.info(f"Documentos carregados: {len(raw_documents)} páginas")

        # Converter dicionários para objetos Document
        documents = []
        for doc_dict in raw_documents:
            doc = Document(
                page_content=doc_dict["page_content"], metadata=doc_dict["metadata"]
            )
            documents.append(doc)

        text_splitter = text_split()
        chunks = generate_chunks(text_splitter, documents)

        # Configurar embeddings e vector store
        embeddings = embedding_config.get_embeddings()
        vector_store = db_config.get_vector_store(embeddings)

        # Adicionar documentos ao vector store
        logger.info("Adicionando chunks ao vector store...")
        vector_store.add_documents(chunks)

        logger.success(f"Ingestão concluída! {len(chunks)} chunks armazenados")

    except Exception as e:
        logger.error(f"Erro na ingestão do PDF: {e}")
        raise


if __name__ == "__main__":
    ingest_pdf()
