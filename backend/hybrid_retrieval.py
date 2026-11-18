
from rank_bm25 import BM25Okapi
from backend.ingestion import load_vector_store


class HybridRetriever:

    def __init__(self, documents):
        self.documents = documents

        # Prepare documents for keyword search
        tokenized_docs = [
            doc.page_content.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(tokenized_docs)

    def search(self, question: str, k: int = 3):

        # 1. BM25 keyword search
        tokenized_query = question.lower().split()

        bm25_scores = self.bm25.get_scores(tokenized_query)

        bm25_results = sorted(
            enumerate(bm25_scores),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        # 2. FAISS semantic search
        vector_store = load_vector_store()

        faiss_results = vector_store.similarity_search(
            question,
            k=k
        )

        # 3. Reciprocal Rank Fusion
        rrf_scores = {}
        documents_map = {}

        def add_ranked_results(results):
            for rank, doc in enumerate(results, start=1):
                key = (
                    doc.metadata.get("source"),
                    doc.metadata.get("page"),
                    doc.page_content
                )

                documents_map[key] = doc

                rrf_scores[key] = (
                    rrf_scores.get(key, 0) +
                    1 / (60 + rank)
                )

        bm25_docs = [
            self.documents[index]
            for index, score in bm25_results
            if score > 0
        ]

        add_ranked_results(bm25_docs)
        add_ranked_results(faiss_results)

        # 4. Return combined ranking
        ranked = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

        return [
            {
                "content": documents_map[key].page_content,
                "source": documents_map[key].metadata.get("source"),
                "page": documents_map[key].metadata.get("page"),
                "rrf_score": score
            }
            for key, score in ranked
        ]


def load_hybrid_retriever():
    vector_store = load_vector_store()

    # Get all indexed documents from FAISS
    docstore = vector_store.docstore

    documents = list(docstore._dict.values())

    if not documents:
        raise ValueError("No documents found in FAISS database.")

    return HybridRetriever(documents)
