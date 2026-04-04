"""POST /query — runs the LangGraph RAG pipeline."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from RAG.shared.db_layer import queries
from RAG.shared.ai_engine.graph.workflow import run_rag_pipeline

router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    session_id: str
    question: str


class QueryResponse(BaseModel):
    session_id: str
    question: str
    answer: str


@router.post("", response_model=QueryResponse)
async def query(request: QueryRequest):
    if not queries.session_exists(request.session_id):
        raise HTTPException(404, f"Session '{request.session_id}' not found. Upload a PDF first.")
    try:
        answer = await run_rag_pipeline(session_id=request.session_id, question=request.question)
    except Exception as exc:
        raise HTTPException(500, f"RAG pipeline error: {exc}") from exc

    return QueryResponse(session_id=request.session_id, question=request.question, answer=answer)
