"""
Central settings — all environment variables live here.
Every other module imports from RAG.shared.config.config, never from dotenv directly.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="RAG/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Groq ─────────────────────────────────────────────────────────────────
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # ── AWS RDS PostgreSQL ────────────────────────────────────────────────────
    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    # ── Embeddings ────────────────────────────────────────────────────────────
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384        # dimension of all-MiniLM-L6-v2

    # ── Chunking ──────────────────────────────────────────────────────────────
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 4

    # ── File uploads ──────────────────────────────────────────────────────────
    upload_dir: str = "RAG/data/uploads"

    # ── FastAPI ───────────────────────────────────────────────────────────────
    api_host: str = "0.0.0.0"
    api_port: int = 8001

    # ── MCP ───────────────────────────────────────────────────────────────────
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000
    mcp_server_url: str = "http://localhost:8000/sse"

    @property
    def database_url(self) -> str:
        """SQLAlchemy connection string for AWS RDS."""
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def async_database_url(self) -> str:
        """Async SQLAlchemy connection string (for future async use)."""
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


# Module-level singleton for convenience
settings = get_settings()
