"""
MCP Client — async context-manager wrapper around FastMCP Client.
Connect to the modular MCP SSE server and call separated RAG tools.
"""

import asyncio
import sys
from typing import Optional

from fastmcp import Client

from RAG.shared.config.config import settings


class RAGMCPClient:
    """
    Async context-manager for the modular RAG MCP server.

    Example:
        async with RAGMCPClient() as client:
            answer = await client.run_rag_query("session-uuid", "What is X?")
            await client.cleanup_session("session-uuid")
    """

    def __init__(self, server_url: Optional[str] = None):
        self._url = server_url or settings.mcp_server_url
        self._client: Optional[Client] = None

    async def __aenter__(self) -> "RAGMCPClient":
        self._client = Client(self._url)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args) -> None:
        if self._client:
            await self._client.__aexit__(*args)

    # ─── Public API ──────────────────────────────────────────────────────────

    async def run_rag_query(self, session_id: str, question: str) -> str:
        """Call the `run_rag_query` MCP tool (from retrieval module)."""
        self._check()
        result = await self._client.call_tool(
            "run_rag_query",
            {"session_id": session_id, "question": question},
        )
        return result.content[0].text if result.content else "(empty response)"

    async def cleanup_session(self, session_id: str) -> str:
        """Call the `cleanup_session_data` MCP tool to clean up RDS data."""
        self._check()
        result = await self._client.call_tool(
            "cleanup_session_data",
            {"session_id": session_id},
        )
        return result.content[0].text if result.content else "(empty response)"

    async def list_tools(self) -> list[str]:
        """Return all modular tool names available on the server."""
        self._check()
        tools = await self._client.list_tools()
        return [t.name for t in tools]

    def _check(self) -> None:
        if self._client is None:
            raise RuntimeError("Use 'async with RAGMCPClient()' first.")


# ─── CLI entry point ─────────────────────────────────────────────────────────

async def _cli() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: python -m RAG.apps.mcp.client <session_id> '<question>'")
        print("       python -m RAG.apps.mcp.client <session_id> --end-session")
        sys.exit(1)

    session_id = args[0]
    async with RAGMCPClient() as client:
        print(f"Connected to {settings.mcp_server_url}")
        print(f"Tools available from modular MCP: {await client.list_tools()}\n")

        if args[1] == "--end-session":
            msg = await client.cleanup_session(session_id)
            print(msg)
        else:
            question = " ".join(args[1:])
            print(f"Q: {question}")
            answer = await client.run_rag_query(session_id, question)
            print(f"A: {answer}")


if __name__ == "__main__":
    asyncio.run(_cli())
