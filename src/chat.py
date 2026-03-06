"""
Chat CLI com busca semântica + LLM.
Uso: python src/chat.py
"""

from config import get_llm
from search import search

EXIT_COMMANDS = ("sair", "exit", "quit")

PROMPT_TEMPLATE = """CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"""


def answer(question: str) -> str:
    results = search(question, k=10)
    context = "\n\n".join(doc.page_content for doc, _ in results)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content


def main():
    print("=" * 50)
    print("  Chat PDF — Digite 'sair' para encerrar")
    print("=" * 50)
    while True:
        print()
        question = input("PERGUNTA: ").strip()
        if not question:
            continue
        if question.lower() in EXIT_COMMANDS:
            print("Encerrando. Até logo!")
            break
        resposta = answer(question)
        print(f"\nRESPOSTA: \n{resposta}")
        print("-" * 50)


if __name__ == "__main__":
    main()
