"""
Embedding service tools for MCP.
"""

from RAG.shared.ai_engine.embeddings import get_embeddings
from typing import List


def generate_embedding(text: str) -> List[float]:
    """
    Generate a 384-dimensional embedding vector for a given piece of text
    using the all-MiniLM-L6-v2 SentenceTransformer model.
    
    Args:
        text: The text string to embed.
    """
    embedder = get_embeddings()
    return embedder.embed_query(text)


def extract_chunks(texts: List[str]) -> str:
    """
    A utility to show how sentences decompose or get embedded.
    
    Args:
        texts: A list of text blocks.
    """
    return f"Prepared {len(texts)} chunks for embedding."
