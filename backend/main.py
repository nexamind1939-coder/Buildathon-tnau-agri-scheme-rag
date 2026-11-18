
from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ingestion import ingest_pdf
from backend.generation import generate_answer


# Initialize application
app = FastAPI(
    title="Velaanmai AI",
    description="Tamil Nadu Agricultural Schemes RAG Assistant",
    version="1.0.0"
)

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to Velaanmai AI",
        "status": "Backend is running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/upload-pdf/")
async def upload_pdf(files: list[UploadFile] = File(...)):
    results = []

    for file in files:
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            results.append({
                "filename": file.filename or "Unknown",
                "status": "failed",
                "message": "Only PDF files are allowed."
            })
            continue

        safe_name = Path(file.filename).name
        unique_name = f"{uuid.uuid4().hex}_{safe_name}"
        file_path = UPLOAD_DIR / unique_name

        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            chunk_count = ingest_pdf(str(file_path))

            results.append({
                "filename": safe_name,
                "status": "success",
                "chunks": chunk_count
            })

        except Exception as error:
            if file_path.exists():
                file_path.unlink()

            results.append({
                "filename": safe_name,
                "status": "failed",
                "message": str(error)
            })

        finally:
            await file.close()

    return {"results": results}


@app.post("/query/")
def query(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        result = generate_answer(question)
        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
