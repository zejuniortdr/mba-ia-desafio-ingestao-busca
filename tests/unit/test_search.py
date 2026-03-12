def test_search_returns_results(mock_vector_store, mock_embeddings):
    from search import search

    results = search("Qual o faturamento?", k=10)
    assert len(results) > 0


def test_search_calls_similarity_with_k(mock_vector_store, mock_embeddings):
    from search import search

    search("pergunta qualquer", k=10)
    mock_vector_store.similarity_search_with_score.assert_called_once_with(
        "pergunta qualquer", k=10
    )


def test_search_result_has_document_and_score(
    mock_vector_store, mock_embeddings, sample_doc
):
    from search import search

    results = search("faturamento", k=10)
    doc, score = results[0]
    assert hasattr(doc, "page_content")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_search_empty_query(mock_vector_store, mock_embeddings):
    mock_vector_store.similarity_search_with_score.return_value = []
    from search import search

    results = search("", k=10)
    assert results == []


def test_search_default_k_is_10(mock_vector_store, mock_embeddings):
    from search import search

    search("qualquer coisa")
    _, kwargs = mock_vector_store.similarity_search_with_score.call_args
    # k pode vir como arg posicional ou keyword
    args, kwargs = mock_vector_store.similarity_search_with_score.call_args
    assert kwargs.get("k") == 10 or (len(args) > 1 and args[1] == 10)
