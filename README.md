# Buildathon tnau-agri-scheme-rag
	Tamil Nadu Agricultural Schemes GenAI Assistant
	
# 🌾 Velaanmai AI – Agricultural Knowledge Assistant

An AI-powered agricultural chatbot designed to help farmers in Tamil Nadu access agricultural scheme information through PDF documents.

Velaanmai AI uses Retrieval-Augmented Generation (RAG), multilingual embeddings, and hybrid search to provide relevant answers in Tamil and English, with source document references.

---

## 📌 Project Overview

Farmers often find it difficult to access and understand information about agricultural schemes, subsidies, eligibility criteria, and government assistance.

Velaanmai AI addresses this problem by allowing users to upload agricultural PDF documents and ask questions in natural language.

The system searches the uploaded documents and generates answers based on the retrieved information.

## 🎯 Objectives

- Make agricultural scheme information easier to access.
- Support Tamil and English questions.
- Allow multiple PDF document uploads.
- Provide answers based on uploaded documents.
- Display source document names and page numbers.
- Reduce incorrect or unsupported AI-generated information.

## ✨ Key Features

- 📄 **Multi-PDF Upload:** Upload multiple agricultural documents.
- 🔍 **PDF Processing:** Extract and split document text into chunks.
- 🌐 **Multilingual Retrieval:** Support Tamil and English document searches.
- 🧠 **RAG Architecture:** Generate answers using retrieved document context.
- 🔎 **Hybrid Search:** Combine BM25 keyword search and FAISS semantic search.
- 📚 **Source References:** Display document names and page numbers.
- 💬 **AI Chatbot:** Ask agricultural questions through a simple interface.
- 🌾 **Farmer-Friendly UI:** Clean and easy-to-use Streamlit application.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | RAG application development |
| FAISS | Vector database |
| Hugging Face | Multilingual embeddings |
| BM25 | Keyword-based retrieval |
| OpenAI | Answer generation |
| FastAPI | Backend API |
| Streamlit | Frontend interface |
| PyPDF | PDF text extraction |

## 🏗️ System Architecture

```text
       User
        |
        v
  Streamlit Frontend
        |
        v
    FastAPI Backend
        |
        v
   PDF Document Upload
        |
        v
    PDF Text Extraction
        |
        v
     Text Chunking
        |
        v
 Multilingual Embeddings
        |
        v
    FAISS Database
        |
        v
   Hybrid Retrieval
    /          \
   v            v
 BM25         FAISS
    \          /
     v        v
  Relevant Documents
        |
        v
   OpenAI LLM
        |
        v
  Generated Answer
        |
        v
 Answer + Source References
```

## 📂 Project Structure

```text
Buildathon-tnau-agri-scheme-rag/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── pdf_processor.py
│   ├── embedding.py
│   ├── ingestion.py
│   ├── retrieval.py
│   ├── hybrid_retrieval.py
│   ├── generation.py
│   └── voice.py
│
├── frontend/
│   ├── app.py
│   └── assets/
│
├── data/
│   ├── faiss_db/
│   ├── metadata/
│   └── uploads/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

```bash
cd YOUR_PROJECT_FOLDER
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
BACKEND_URL=http://127.0.0.1:8000
```

Never upload your real API key to GitHub.

### 6. Start the Backend

Open the first terminal:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Backend API:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the Frontend

Open a second terminal and activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Run Streamlit:

```bash
python -m streamlit run frontend/app.py
```

Open the application:

```text
http://localhost:8501
```

## 💬 How to Use

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Open the Velaanmai AI application.
4. Navigate to Document Centre.
5. Upload agricultural scheme PDF documents.
6. Wait for document processing and indexing.
7. Open AI Assistant.
8. Ask questions in Tamil or English.
9. Read the generated answer and check its source references.

## 📝 Example Questions

**English:**
- What agricultural support is available for farmers?
- What machinery assistance is available?
- What irrigation schemes are mentioned in the documents?

**Tamil:**
- விவசாயிகளுக்கு என்ன உதவிகள் கிடைக்கின்றன?
- விவசாய இயந்திரங்களுக்கு மானியம் கிடைக்குமா?
- பாசன வசதிகளுக்கு என்ன திட்டங்கள் உள்ளன?

## 🔮 Future Enhancements

- Voice-based questions and answers.
- Tamil speech-to-text and text-to-speech.
- Government scheme eligibility checking.
- Improved Tamil keyword search.
- More agricultural document collections.
- Mobile-friendly interface.
- User authentication and chat history storage.

## ⚠️ Disclaimer

Velaanmai AI is an independent educational and development project.

It is not an official Government of Tamil Nadu or Tamil Nadu Agricultural University (TNAU) website.

The answers depend on the uploaded documents. Users should verify scheme eligibility, benefits, and application procedures with the relevant official authorities.

---

## 👩‍💻 Project Information

**Project Name:** Velaanmai AI  
**Domain:** Agriculture + Artificial Intelligence  
**Category:** Generative AI / RAG Chatbot  
**Primary Goal:** Making agricultural scheme information accessible to farmers in Tamil Nadu.

---

