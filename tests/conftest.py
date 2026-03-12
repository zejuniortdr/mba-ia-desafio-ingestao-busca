import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Garante que src/ esteja no path para importar config, search, etc.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def mock_embeddings():
    embeddings = MagicMock()
    embeddings.embed_query.return_value = [0.1] * 1536
    embeddings.embed_documents.return_value = [[0.1] * 1536]

    with (
        patch("search.get_embeddings", return_value=embeddings),
        patch("config.get_embeddings", return_value=embeddings),
    ):
        yield embeddings


@pytest.fixture
def mock_llm():
    with patch("chat.get_llm") as m:
        llm = MagicMock()
        llm.invoke.return_value = MagicMock(
            content="Faturamento foi de 10 milhoes de reais."
        )
        m.return_value = llm
        yield llm


@pytest.fixture
def sample_doc():
    doc = MagicMock()
    doc.page_content = (
        "O faturamento da Empresa SuperTechIABrazil foi de 10 milhoes de reais."
    )
    doc.metadata = {"page": 0, "source": "document.pdf"}
    return doc


@pytest.fixture
def mock_vector_store(sample_doc):
    vs = MagicMock()
    vs.similarity_search_with_score.return_value = [(sample_doc, 0.95)]

    with (
        patch("langchain_postgres.PGVector", return_value=vs),
        patch("search.get_vector_store", return_value=vs),
    ):
        yield vs
