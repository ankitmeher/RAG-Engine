"""
PDF ingestion — loads, splits, embeds and stores chunks in RDS.
Pure psycopg2, no SQLAlchemy.
"""

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from RAG.shared.config.config import settings
from RAG.shared.ai_engine.embeddings import get_embeddings
from RAG.shared.db_layer import queries


def ingest_pdf(file_path: str, session_id: str) -> dict:
    """
    Full pipeline → returns ingestion summary dict.
    1. Ensure session exists in RDS.
    2. Load PDF pages.
    3. Split into chunks.
    4. Embed all chunks (SentenceTransformer).
    5. Bulk-insert into document_chunks table.
    """
    # Ensure session row exists
    queries.create_session(session_id)

    # Load
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    chunks = splitter.split_documents(pages)
    if not chunks:
        return {"session_id": session_id, "chunks_ingested": 0}

    texts = [c.page_content for c in chunks]
    source_file = os.path.basename(file_path)
    names = [f"{source_file}_chunk_{i}" for i in range(len(texts))]

    # Embed
    embedder = get_embeddings()
    embeddings = embedder.embed_documents(texts)

    # Store
    ids = queries.insert_chunks(
        session_id=session_id,
        texts=texts,
        chunk_names=names,
        source_file=source_file,
        embeddings=embeddings,
    )

    return {
        "session_id": session_id,
        "source_file": source_file,
        "chunks_ingested": len(chunks),
        "chunk_ids": ids,
    }
