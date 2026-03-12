"""
Testes de integracao: requerem banco PostgreSQL rodando.
Execute com: make test-integration  (apos docker compose up -d)
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

# Pula todos os testes deste modulo se nao houver conexao com o banco
pytest.importorskip("psycopg")


def _db_available():
    try:
        import psycopg

        from config import CONNECTION_STRING

        conn = psycopg.connect(CONNECTION_STRING)
        conn.close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _db_available(),
    reason="Banco PostgreSQL nao disponivel. Rode: docker compose up -d",
)


def test_vector_store_connects():
    from config import get_embeddings, get_vector_store

    embeddings = get_embeddings()
    vs = get_vector_store(embeddings)
    assert vs is not None


def test_search_returns_list():
    from search import search

    results = search("faturamento", k=3)
    assert isinstance(results, list)


def test_full_pipeline_ingest_and_search(tmp_path):
    """Cria um PDF minimo, ingere e busca para validar o pipeline completo."""
    from fpdf import FPDF

    from config import get_embeddings, get_vector_store

    # Cria PDF temporario
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(
        200, 10, txt="O faturamento da Empresa TesteCo foi de 42 milhoes.", ln=True
    )
    pdf_path = tmp_path / "test_doc.pdf"
    pdf.output(str(pdf_path))

    # Ingere
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(pages)

    embeddings = get_embeddings()
    vs = get_vector_store(embeddings)
    vs.add_documents(chunks)

    # Busca
    results = vs.similarity_search_with_score("faturamento TesteCo", k=3)
    assert len(results) > 0
    texts = [doc.page_content for doc, _ in results]
    assert any("42 milhoes" in t or "TesteCo" in t for t in texts)
