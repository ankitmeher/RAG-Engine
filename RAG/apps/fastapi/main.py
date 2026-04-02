"""
FastAPI application — entry point.
Run with: uvicorn RAG.main:app --reload --port 8001
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from RAG.apps.fastapi.api.routes import health, query, session, upload
from RAG.shared.db_layer.init_db import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Enable pgvector extension and create tables on startup."""
    init_db()
    yield


app = FastAPI(
    title="RAG Web App API",
    description="Upload PDFs and query them via LangGraph + Groq + pgvector on AWS RDS.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS (React dev servers) ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # CRA
        "http://localhost:5173",   # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(upload.router)
app.include_router(query.router)
app.include_router(session.router)
