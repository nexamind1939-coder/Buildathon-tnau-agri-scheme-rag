
from backend.ingestion import load_vector_store


def retrieve_documents(question: str, k: int = 3):
    """Find the most relevant PDF chunks for a question."""

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    retrieved_data = []

    for document, score in results:
        retrieved_data.append({
            "content": document.page_content,
            "source": document.metadata.get("source", "Unknown"),
            "page": document.metadata.get("page", "Unknown"),
            "score": float(score)
        })

    return retrieved_data
