from unittest.mock import MagicMock, patch

import pytest
from langchain_core.documents import Document


@pytest.fixture
def sample_pages():
    return [
        Document(
            page_content="Pagina 1 com muito conteudo de teste " * 30,
            metadata={"page": 0},
        ),
        Document(
            page_content="Pagina 2 com outro conteudo relevante " * 30,
            metadata={"page": 1},
        ),
    ]


def test_pdf_is_split_into_chunks(sample_pages):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(sample_pages)
    assert len(chunks) > 0
    for chunk in chunks:
        assert len(chunk.page_content) <= 1000


def test_chunk_overlap_is_applied(sample_pages):
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(sample_pages)
    if len(chunks) > 1:
        # O inicio do segundo chunk deve ter conteudo
        # que tambem aparece no final do primeiro
        end_of_first = chunks[0].page_content[-150:]
        start_of_second = chunks[1].page_content[:150]
        assert any(word in start_of_second for word in end_of_first.split()[:5])


def test_ingest_calls_add_documents(mock_vector_store, mock_embeddings):
    with (
        patch("ingest.PyPDFLoader") as mock_loader_cls,
        patch("ingest.PDF_PATH", "document.pdf"),
    ):
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            Document(page_content="Conteudo de teste " * 60, metadata={"page": 0}),
        ]
        mock_loader_cls.return_value = mock_loader

        from ingest import ingest_pdf

        ingest_pdf()

        assert mock_vector_store.add_documents.called


def test_ingest_uses_correct_chunk_settings(mock_vector_store, mock_embeddings):
    with (
        patch("ingest.PyPDFLoader") as mock_loader_cls,
        patch("ingest.RecursiveCharacterTextSplitter") as mock_splitter_cls,
        patch("ingest.PDF_PATH", "document.pdf"),
    ):
        mock_loader = MagicMock()
        mock_loader.load.return_value = [
            Document(page_content="x" * 500, metadata={"page": 0}),
        ]
        mock_loader_cls.return_value = mock_loader

        mock_splitter = MagicMock()
        mock_splitter.split_documents.return_value = [
            Document(page_content="x" * 500, metadata={"page": 0}),
        ]
        mock_splitter_cls.return_value = mock_splitter

        from ingest import ingest_pdf

        ingest_pdf()

        mock_splitter_cls.assert_called_once_with(chunk_size=1000, chunk_overlap=150)
