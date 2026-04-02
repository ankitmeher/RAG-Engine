"""
Vector store management tools for MCP.
"""
from typing import List
from RAG.shared.db_layer import queries


def search_vector_store(session_id: str, query: str, k: int = 4) -> List[str]:
    """
    Directly query the pgvector database for the most semantically similar chunks
    within a specific session, without running the full LLM pipeline.
    
    Args:
        session_id: The UUID of the uploaded document session.
        query: The semantic search query.
        k: Number of chunks to return (default is 4).
    """
    from RAG.shared.ai_engine.embeddings import get_embeddings
    embedder = get_embeddings()
    query_vec = embedder.embed_query(query)
    
    return queries.cosine_search(session_id, query_vec, k)


def list_session_chunks(session_id: str) -> str:
    """
    List all document chunks stored in the vector database for a session.
    
    Args:
        session_id: The session UUID.
    """
    chunks = queries.get_chunks_by_session(session_id)
    if not chunks:
        return "No chunks found for this session."
    
    summary = [f"{c['chunk_name']} (from {c['source_file']})" for c in chunks]
    return f"Total chunks: {len(summary)}\n" + "\n".join(summary)


def cleanup_session_data(session_id: str) -> str:
    """
    Delete all chunks, vectors, and session metadata from the database.
    
    Args:
        session_id: The session UUID.
    """
    if not queries.session_exists(session_id):
        return f"Session '{session_id}' not found."
    
    deleted_count = queries.delete_session(session_id)
    return f"Session deleted successfully. Removed {deleted_count} vector chunks."
