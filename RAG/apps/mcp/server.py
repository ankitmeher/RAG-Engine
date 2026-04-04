"""
MCP Microservice — Stable FastAPI Implementation.
A rock-solid microservice for RAG tool calling.
Works 100% with AWS Lambda (Mangum) and local development.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

from RAG.apps.mcp.tools import retrieval
from RAG.shared.db_layer.init_db import init_db
from RAG.shared.ai_engine.embeddings import get_embeddings
from contextlib import asynccontextmanager

# ── Setup ───────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Enable pgvector and pre-load the AI models into memory."""
    init_db()
    print("--- [MCP SERVER] Warming up AI models... ---")
    get_embeddings() # Pre-load the HuggingFace model
    print("--- [MCP SERVER] All models loaded! ---")
    yield

app = FastAPI(title="RAG-MCP-Microservice", lifespan=lifespan)
handler = Mangum(app)  # Entry point for AWS Lambda


# ── Tool Definitions ─────────────────────────────────────────────────────────

class ToolCallRequest(BaseModel):
    tool: str
    arguments: dict


@app.post("/call")
async def call_tool(request: ToolCallRequest):
    """Stateless entry point to execute RAG tools."""
    t_name = request.tool.lower()
    args = request.arguments
    
    print(f"--- [MCP SERVER] Received call for: {t_name} ---")
    
    try:
        if t_name == "search_vector_store":
            return await retrieval.search_vector_store(
                session_id=args["session_id"],
                query=args["query"],
                k=args.get("k", 4)
            )
        
        elif t_name == "run_rag_query":
            return await retrieval.run_rag_query(
                session_id=args["session_id"],
                question=args["question"]
            )
            
        elif t_name == "cleanup_session_data":
            return await retrieval.cleanup_session_data(
                session_id=args["session_id"]
            )
            
        else:
            raise HTTPException(404, f"Tool '{t_name}' not found on this server.")
            
    except Exception as e:
        print(f"--- [MCP SERVER] Tool Error: {e} ---")
        raise HTTPException(500, str(e))


@app.get("/")
async def health():
    return {"status": "ok", "service": "RAG-MCP-Microservice", "transport": "Pure HTTP"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
