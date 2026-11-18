
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="Velaanmai AI",
    page_icon="🌾",
    layout="wide"
)

# Three-colour theme: green, white and black
st.markdown("""
<style>
.stApp {
    background: #FFFFFF;
    color: #000000;
}

[data-testid="stSidebar"] {
    background: #176B3A;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

h1, h2, h3, h4, p, label, li, .stMarkdown {
    color: #000000 !important;
}

.hero {
    background: #176B3A;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.hero h1, .hero p {
    color: #FFFFFF !important;
}

.stButton button {
    background: #176B3A !important;
    color: #FFFFFF !important;
    border: 1px solid #176B3A !important;
    border-radius: 8px;
}

.stButton button:hover {
    background: #000000 !important;
    color: #FFFFFF !important;
}

[data-testid="stChatMessage"],
[data-testid="stExpander"],
[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px solid #000000;
    border-radius: 10px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #000000 !important;
}

[data-testid="stChatInput"] textarea,
.stTextInput input,
.stTextArea textarea {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #000000 !important;
}

.disclaimer {
    background: #176B3A;
    color: #FFFFFF !important;
    padding: 15px;
    border-radius: 10px;
}

.disclaimer strong {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_documents" not in st.session_state:
    st.session_state.uploaded_documents = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# Backend status
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False


backend_online = check_backend()


# Sidebar
with st.sidebar:
    st.markdown("# 🌾 Velaanmai AI")
    st.caption("Agricultural Knowledge Assistant")

    st.divider()

    page = st.radio(
        "Navigation",
        ["AI Assistant", "Document Centre", "Chat History"]
    )

    language = st.selectbox(
        "Response Language",
        ["Tamil", "English", "Tamil + English"]
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Independent AI project")
    st.caption("Not an official Government of Tamil Nadu website.")


# Header
st.markdown("""
<div class="hero">
    <h1>🌾 வேளாண்மை தோழன் AI</h1>
    <p>Your Intelligent Agricultural Schemes Assistant</p>
    <p>Ask Questions • Upload PDFs • Discover Agricultural Information</p>
</div>
""", unsafe_allow_html=True)


# Connection status
if backend_online:
    st.success("Backend Connected")
else:
    st.error("Backend Offline. Start FastAPI on port 8000.")


# AI Assistant
if page == "AI Assistant":

    st.subheader("💬 Ask Your Agricultural Question")

    st.write("Ask questions about agricultural schemes and farmer assistance.")

    # Previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View Sources"):
                    for source in message["sources"]:
                        st.write(
                            f"{source['source']} | Page {source['page']}"
                        )

    # Suggested questions
    with st.expander("Suggested Questions"):
        suggestions = [
            "What support is available for farmers?",
            "What machinery assistance is available?",
            "What irrigation schemes are available?",
            "விவசாயிகளுக்கு என்ன உதவிகள் கிடைக்கின்றன?"
        ]

        for i, suggestion in enumerate(suggestions):
            if st.button(suggestion, key=f"suggest_{i}"):
                st.session_state.pending_question = suggestion
                st.rerun()

    question = st.chat_input("Type your question in Tamil or English...")

    if not question and st.session_state.pending_question:
        question = st.session_state.pending_question
        st.session_state.pending_question = None

    if question:

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            if not backend_online:
                answer = "Backend is offline. Please start FastAPI."
                st.error(answer)

            else:
                try:
                    with st.spinner("Searching agricultural documents..."):
                        response = requests.post(
                            f"{BACKEND_URL}/query/",
                            json={"question": question},
                            timeout=180
                        )
                        response.raise_for_status()
                        result = response.json()

                    answer = result.get("answer", "No answer returned.")
                    sources = result.get("sources", [])

                    st.markdown(answer)

                    if sources:
                        with st.expander("View Sources"):
                            for source in sources:
                                st.write(
                                    f"{source['source']} | Page {source['page']}"
                                )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except requests.HTTPError as error:
                    answer = f"Backend error: {error}"
                    st.error(answer)

                except requests.RequestException as error:
                    answer = f"Connection error: {error}"
                    st.error(answer)

                except Exception as error:
                    answer = f"Unexpected error: {error}"
                    st.error(answer)

            if not backend_online:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })


# Document Centre
elif page == "Document Centre":

    st.subheader("📚 Agricultural Document Centre")

    st.write("Upload PDF documents to build your agricultural knowledge base.")

    uploaded_files = st.file_uploader(
        "Choose PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button(
        "Upload and Process Documents",
        disabled=not uploaded_files or not backend_online
    ):

        files_to_upload = [
            ("files", (file.name, file.getvalue(), "application/pdf"))
            for file in uploaded_files
        ]

        try:
            with st.spinner("Processing documents..."):
                response = requests.post(
                    f"{BACKEND_URL}/upload-pdf/",
                    files=files_to_upload,
                    timeout=300
                )
                response.raise_for_status()
                results = response.json().get("results", [])

            for result in results:
                if result["status"] == "success":
                    st.success(
                        f"{result['filename']} - {result['chunks']} chunks indexed"
                    )

                    if result["filename"] not in st.session_state.uploaded_documents:
                        st.session_state.uploaded_documents.append(
                            result["filename"]
                        )
                else:
                    st.error(
                        f"{result['filename']}: {result.get('message', 'Upload failed')}"
                    )

        except requests.RequestException as error:
            st.error(f"Upload error: {error}")

    st.divider()
    st.subheader("Uploaded Documents")

    if st.session_state.uploaded_documents:
        for filename in st.session_state.uploaded_documents:
            st.write(f"📄 {filename}")
    else:
        st.info("No documents uploaded in this session.")


# Chat History
elif page == "Chat History":

    st.subheader("🕘 Chat History")

    if st.session_state.messages:
        for message in st.session_state.messages:
            role = "You" if message["role"] == "user" else "Velaanmai AI"

            st.markdown(f"**{role}**")
            st.write(message["content"])
            st.divider()
    else:
        st.info("No conversations yet.")


# Footer
st.divider()

st.markdown("""
<div class="disclaimer">
    <strong>Disclaimer:</strong>
    Velaanmai AI is an independent AI project, not an official
    Government of Tamil Nadu or TNAU website.
    Please verify scheme details with the relevant authorities.
</div>
""", unsafe_allow_html=True)

st.caption("🌾 Velaanmai AI | Agricultural Knowledge Assistant")
