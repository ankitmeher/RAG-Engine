async def run_rag_query(session_id: str, question: str) -> str:
    """Run the complete LangGraph RAG pipeline."""
    from RAG.shared.ai_engine.graph.workflow import run_rag_pipeline
    try:
        return await run_rag_pipeline(session_id=session_id, question=question)
    except Exception as exc:
        return f"Error running RAG pipeline: {exc}"


async def search_vector_store(session_id: str, query: str, k: int = 4) -> list[str]:
    """Retrieve relevant chunks directly from the vector store."""
    from RAG.shared.db_layer import queries
    from RAG.shared.ai_engine.embeddings import get_embeddings
    try:
        # 1. Turn text into a numerical vector (embedding)
        embedder = get_embeddings()
        query_vector = embedder.embed_query(query)
        
        # 2. Search the database with the vector
        return queries.cosine_search(
            session_id=session_id, 
            query_embedding=query_vector, 
            k=k
        )
    except Exception as exc:
        return [f"Error searching vector store: {exc}"]


async def cleanup_session_data(session_id: str) -> str:
    """Wipe all chunks and session records from the database."""
    from RAG.shared.db_layer import queries
    try:
        count = queries.delete_session(session_id)
        return f"Session {session_id} data cleared. Deleted {count} chunks."
    except Exception as exc:
        return f"Error cleaning up session: {exc}"
