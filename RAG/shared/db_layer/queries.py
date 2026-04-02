"""
All raw SQL query functions.
Nothing else in the project writes SQL — import from here.
"""

import uuid
from typing import List, Optional

import psycopg2.extras

from RAG.shared.db_layer.connection import get_conn


# ─────────────────────────── Session ────────────────────────────────────────

def create_session(session_id: str) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO user_sessions (session_id) VALUES (%s) ON CONFLICT DO NOTHING;",
                (session_id,),
            )


def session_exists(session_id: str) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM user_sessions WHERE session_id = %s;",
                (session_id,),
            )
            return cur.fetchone() is not None


def delete_session(session_id: str) -> int:
    """
    Delete the session AND all its chunks (via ON DELETE CASCADE).
    Returns the number of chunks deleted.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM document_chunks WHERE session_id = %s;",
                (session_id,),
            )
            count = cur.fetchone()[0]
            cur.execute(
                "DELETE FROM user_sessions WHERE session_id = %s;",
                (session_id,),
            )
            return count


# ─────────────────────────── Chunks ─────────────────────────────────────────

def insert_chunks(
    session_id: str,
    texts: List[str],
    chunk_names: List[str],
    source_file: str,
    embeddings: List[List[float]],
) -> List[str]:
    """
    Bulk-insert chunk rows. Returns list of generated UUIDs.
    """
    rows = [
        (
            str(uuid.uuid4()),
            session_id,
            name,
            source_file,
            text[:200],        # content_preview
            emb,
        )
        for text, name, emb in zip(texts, chunk_names, embeddings)
    ]
    ids = [r[0] for r in rows]

    with get_conn() as conn:
        psycopg2.extras.execute_values(
            conn.cursor(),
            """
            INSERT INTO document_chunks
                (id, session_id, chunk_name, source_file, content_preview, embedding)
            VALUES %s;
            """,
            rows,
        )
    return ids


def get_chunks_by_session(session_id: str) -> List[dict]:
    """Return lightweight metadata for all chunks in a session."""
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, chunk_name, source_file, content_preview, created_at
                FROM document_chunks
                WHERE session_id = %s
                ORDER BY created_at;
                """,
                (session_id,),
            )
            return [dict(r) for r in cur.fetchall()]


def cosine_search(
    session_id: str,
    query_embedding: List[float],
    k: int = 10,
) -> List[str]:
    """
    Return the top-k most similar content_preview texts for a session.
    Uses pgvector <=> (cosine distance) operator.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT content_preview
                FROM document_chunks
                WHERE session_id = %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                (session_id, query_embedding, k),
            )
            return [row[0] for row in cur.fetchall()]
