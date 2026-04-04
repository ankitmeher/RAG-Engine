"""
MCP Client — Stateless HTTP implementation.
Connects to the modular MCP server via JSON-RPC over HTTP.
Perfect for AWS Lambda (Mangum) and local HTTP transport.
"""

import asyncio
import sys
import httpx
from typing import Optional, Any

from RAG.shared.config.config import settings


class RAGMCPClient:
    """
    Stateless HTTP Client for the modular RAG MCP server.
    Uses JSON-RPC 2.0 over HTTP.
    """

    def __init__(self, server_url: Optional[str] = None):
        base_url = server_url or settings.mcp_server_url
        self._url = f"{base_url.rstrip('/')}/call"
        self._client = httpx.AsyncClient(timeout=120.0)

    async def __aenter__(self) -> "RAGMCPClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self._client.aclose()

    # ─── Public API ──────────────────────────────────────────────────────────

    async def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Low-level POST call to execute a microservice tool."""
        # Standard JSON request for our new FastAPI microservice
        payload = {
            "tool": tool_name,
            "arguments": arguments
        }
        
        response = await self._client.post(self._url, json=payload)
        response.raise_for_status()
        
        # The new server returns the result directly (no result/content wrapper)
        return response.json()

    async def run_rag_query(self, session_id: str, question: str) -> str:
        """Call the `run_rag_query` tool."""
        # result is now directly the answer string
        return await self.call_tool("run_rag_query", {
            "session_id": session_id,
            "question": question
        })

    async def search_vector_store(self, session_id: str, query: str, k: int = 4) -> list[str]:
        """Call the `search_vector_store` tool."""
        # result is now directly the list of strings
        return await self.call_tool("search_vector_store", {
            "session_id": session_id,
            "query": query,
            "k": k
        })

    async def cleanup_session(self, session_id: str) -> str:
        """Call the `cleanup_session_data` tool."""
        # result is now directly the success message
        return await self.call_tool("cleanup_session_data", {
            "session_id": session_id
        })


# ─── CLI entry point ─────────────────────────────────────────────────────────

async def _cli() -> None:
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python -m RAG.apps.mcp.client <session_id> '<question>'")
        sys.exit(1)

    session_id = args[0]
    async with RAGMCPClient() as client:
        print(f"Connecting to {settings.mcp_server_url}")
        
        if len(args) > 1 and args[1] == "--end-session":
            msg = await client.cleanup_session(session_id)
            print(f"Cleanup: {msg}")
        else:
            question = " ".join(args[1:]) if len(args) > 1 else "Hello"
            print(f"Q: {question}")
            answer = await client.run_rag_query(session_id, question)
            print(f"A: {answer}")


if __name__ == "__main__":
    asyncio.run(_cli())
