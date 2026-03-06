"""
Busca semântica direta (sem LLM).
Uso: python src/search.py "sua pergunta aqui"
"""

import sys

from config import get_embeddings, get_vector_store


def search(query: str, k: int = 10):
    embeddings = get_embeddings()
    vector_store = get_vector_store(embeddings)
    results = vector_store.similarity_search_with_score(query, k=k)
    return results


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Pergunta: ")
    results = search(query)
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n--- Resultado {i} (score: {score:.4f}) ---")
        print(doc.page_content[:300])
