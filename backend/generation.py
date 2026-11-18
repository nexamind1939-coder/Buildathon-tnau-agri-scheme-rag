
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from backend.hybrid_retrieval import load_hybrid_retriever

load_dotenv()


def generate_answer(question: str):
    """Generate a grounded answer using retrieved agricultural documents."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        raise ValueError(
            "Please add your valid OPENAI_API_KEY to the .env file."
        )

    # Retrieve relevant document chunks
    retriever = load_hybrid_retriever()
    results = retriever.search(question, k=4)

    if not results:
        return {
            "answer": "The uploaded documents do not contain enough information to answer this question.",
            "sources": []
        }

    # Prepare document context
    context = "\n\n".join(
        [
            f"Source: {item['source']}, Page: {item['page']}\n"
            f"Content: {item['content']}"
            for item in results
        ]
    )

    # Initialize language model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    system_prompt = """
You are Velaanmai AI, an agricultural information assistant
for Tamil Nadu farmers.

Rules:
1. Answer only using the supplied document context.
2. Never invent government schemes, subsidies, amounts,
   eligibility rules or application procedures.
3. If the documents do not contain the answer, clearly say so.
4. Answer in the same language as the user's question.
5. Explain information in simple language.
6. Mention relevant source filenames and page numbers.
7. Do not claim to be an official government service.

The project is independent and is not an official
Government of Tamil Nadu website.
"""

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Question:
{question}

Retrieved document context:
{context}

Provide a clear answer based only on this context.
""")
    ])

    # Prepare source references
    sources = [
        {
            "source": item["source"],
            "page": item["page"]
        }
        for item in results
    ]

    return {
        "answer": response.content,
        "sources": sources
    }
