"""
One-time DB initialisation.
Enables the pgvector extension and creates all tables if they don't exist.
Safe to call on every startup (idempotent).
"""

from RAG.shared.db_layer.connection import get_conn


DDL = """
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- User sessions table
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id  VARCHAR(64)  PRIMARY KEY,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Document chunks table
-- Each row stores one text chunk + its embedding vector for a session
CREATE TABLE IF NOT EXISTS document_chunks (
    id              UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      VARCHAR(64)  NOT NULL REFERENCES user_sessions(session_id) ON DELETE CASCADE,
    chunk_name      VARCHAR(255) NOT NULL,
    source_file     VARCHAR(255) NOT NULL,
    content_preview TEXT,
    embedding       VECTOR(384),              -- all-MiniLM-L6-v2 dimension
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- Index for fast cosine search scoped to a session
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON document_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Index for fast session-based lookups
CREATE INDEX IF NOT EXISTS idx_chunks_session
    ON document_chunks (session_id);
"""


def init_db() -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(DDL)
