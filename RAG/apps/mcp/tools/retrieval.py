"""
Retrieval and Agentic (RAG) tools for MCP.
"""

from RAG.shared.ai_engine.graph.workflow import run_rag_pipeline
from RAG.shared.db_layer import queries


def run_rag_query(session_id: str, question: str) -> str:
    """
    Run the complete LangGraph RAG pipeline: retrieves chunks via pgvector 
    and synthesizes an answer using the Groq Llama-3 LLM.
    
    Args:
        session_id: The UUID returned when a PDF was uploaded.
        question: Natural-language question about the documents.
    """
    try:
        return run_rag_pipeline(session_id=session_id, question=question)
    except Exception as exc:
        return f"Error running RAG pipeline: {exc}"
