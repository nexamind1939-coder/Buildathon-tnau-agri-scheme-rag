
from pathlib import Path
from langchain_community.vectorstores import FAISS

from backend.pdf_processor import process_pdf
from backend.embedding import get_embeddings


DB_PATH = Path("data/faiss_db")


def ingest_pdf(file_path: str):
    """Add a PDF to the existing FAISS database."""

    chunks = process_pdf(file_path)
    embeddings = get_embeddings()

    DB_PATH.mkdir(parents=True, exist_ok=True)

    if (DB_PATH / "index.faiss").exists():
        vector_store = FAISS.load_local(
            str(DB_PATH),
            embeddings,
            allow_dangerous_deserialization=True
        )

        vector_store.add_documents(chunks)

    else:
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

    vector_store.save_local(str(DB_PATH))

    return len(chunks)


def load_vector_store():
    """Load the saved FAISS database."""

    if not (DB_PATH / "index.faiss").exists():
        raise FileNotFoundError(
            "FAISS database not found. Upload a PDF first."
        )

    embeddings = get_embeddings()

    return FAISS.load_local(
        str(DB_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

