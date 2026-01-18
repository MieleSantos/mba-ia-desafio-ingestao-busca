import os

from dotenv import load_dotenv

from pdf_loader import PDFLoader

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")


def ingest_pdf() -> None:
    if not PDF_PATH:
        print("Error: PDF_PATH not configured in .env file")
        return

    try:
        pdf = PDFLoader(PDF_PATH)
        text = pdf.load_text()
        print(f"Successfully loaded PDF with {len(text)} characters")
        print(f"First 200 chars: {text[:200]}")
    except Exception as e:
        print(f"Error loading PDF: {e}")


if __name__ == "__main__":
    ingest_pdf()
