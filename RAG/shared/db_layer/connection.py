"""
psycopg2 connection context manager.
All DB operations import from here — no SQLAlchemy, no ORM overhead.
"""

from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras
from pgvector.psycopg2 import register_vector

from RAG.shared.config.config import settings


@contextmanager
def get_conn() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Yield a psycopg2 connection to AWS RDS.
    - Registers pgvector type adapters automatically.
    - Commits on success, rolls back on exception, always closes.
    """
    conn = psycopg2.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        connect_timeout=10,
    )
    register_vector(conn)          # enables <=> cosine operator + Python list ↔ VECTOR
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
