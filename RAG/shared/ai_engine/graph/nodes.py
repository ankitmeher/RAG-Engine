"""
LangGraph nodes — retrieve via pgvector, generate via Groq.
Uses psycopg2 queries directly; no SQLAlchemy.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from RAG.shared.config.config import settings
from RAG.shared.ai_engine.embeddings import get_embeddings
from RAG.shared.db_layer import queries
from RAG.shared.ai_engine.graph.state import RAGState

_llm: ChatGroq | None = None


def _get_llm() -> ChatGroq:
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            model=settings.groq_model,
            temperature=0,
            api_key=settings.groq_api_key,
        )
    return _llm


# ── Node 1: Retrieve ─────────────────────────────────────────────────────────

def retrieve_node(state: RAGState) -> dict:
    embedder = get_embeddings()
    query_vec = embedder.embed_query(state["question"])
    chunks = queries.cosine_search(
        session_id=state["session_id"],
        query_embedding=query_vec,
        k=settings.top_k,
    )
    context = "\n\n".join(chunks) if chunks else "No relevant context found."
    return {"context": context}


# ── Node 2: Generate ─────────────────────────────────────────────────────────

_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful AI assistant. 
Below is some retrieved context from uploaded documents. 
If the context is relevant, use it to answer the question. 
If no context is provided, or the context isn't relevant to the question, use your general knowledge to answer.

Context:
{context}

Question: {question}
Answer:
""")


def generate_node(state: RAGState) -> dict:
    chain = _PROMPT | _get_llm()
    response = chain.invoke({
        "context": state["context"],
        "question": state["question"],
    })
    return {"answer": response.content}
