"""
Ingestão do PDF no banco pgVector.
Uso: python src/ingest.py
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE, PDF_PATH, get_embeddings, get_vector_store


def ingest_pdf():
    print(f"[ingest] Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    print(f"[ingest] {len(pages)} página(s) carregada(s)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(pages)
    print(f"[ingest] {len(chunks)} chunk(s) gerado(s)")

    print("[ingest] Conectando ao pgVector e salvando embeddings...")
    embeddings = get_embeddings()
    vector_store = get_vector_store(embeddings)
    vector_store.add_documents(chunks)

    print(f"[ingest] Concluído! {len(chunks)} chunks armazenados no banco.")


if __name__ == "__main__":
    ingest_pdf()
