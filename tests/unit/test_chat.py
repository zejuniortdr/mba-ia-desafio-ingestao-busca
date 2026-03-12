from unittest.mock import MagicMock


def test_answer_uses_context_from_search(
    mock_vector_store, mock_embeddings, mock_llm, sample_doc
):
    from chat import answer

    result = answer("Qual o faturamento?")
    assert isinstance(result, str)
    assert len(result) > 0


def test_answer_calls_llm_with_prompt(
    mock_vector_store, mock_embeddings, mock_llm, sample_doc
):
    from chat import answer

    answer("Qual o faturamento?")
    assert mock_llm.invoke.called
    prompt_used = mock_llm.invoke.call_args[0][0]
    assert "CONTEXTO:" in prompt_used
    assert "REGRAS:" in prompt_used
    assert "PERGUNTA DO USUÁRIO:" in prompt_used


def test_prompt_contains_search_context(
    mock_vector_store, mock_embeddings, mock_llm, sample_doc
):
    from chat import answer

    answer("Qual o faturamento?")
    prompt_used = mock_llm.invoke.call_args[0][0]
    assert sample_doc.page_content in prompt_used


def test_prompt_contains_user_question(mock_vector_store, mock_embeddings, mock_llm):
    from chat import answer

    question = "Qual o faturamento da empresa?"
    answer(question)
    prompt_used = mock_llm.invoke.call_args[0][0]
    assert question in prompt_used


def test_out_of_context_response(mock_vector_store, mock_embeddings, mock_llm):
    mock_llm.invoke.return_value = MagicMock(
        content="Nao tenho informacoes necessarias para responder sua pergunta."
    )
    from chat import answer

    result = answer("Qual a capital da Franca?")
    assert "Nao tenho informacoes" in result


def test_answer_returns_llm_content_string(
    mock_vector_store, mock_embeddings, mock_llm
):
    expected = "Faturamento foi de 10 milhoes de reais."
    mock_llm.invoke.return_value = MagicMock(content=expected)
    from chat import answer

    result = answer("faturamento")
    assert result == expected
