"""
MCP Server Entry Point over HTTP transport.
Suitable for AWS Lambda deployment via Mangum adapter or running natively as a web server.
"""

from fastmcp import FastMCP

from RAG.shared.config.config import settings
from mangum import Mangum


# Import modular tools
from RAG.apps.mcp.tools import vector_store
from RAG.apps.mcp.tools import retrieval
from RAG.apps.mcp.tools import embedding

# Create the MCP application
mcp = FastMCP("RAG-Modular-Agent-MCP")

# ─────────────────────────── Register Tools ───────────────────────────

# 1. Retrieval (Core RAG)
mcp.tool()(retrieval.run_rag_query)

# 2. Vector Store Management
mcp.tool()(vector_store.search_vector_store)
mcp.tool()(vector_store.list_session_chunks)
mcp.tool()(vector_store.cleanup_session_data)

# 3. Embeddings/Analytics
mcp.tool()(embedding.generate_embedding)


# ─────────────────────────── Server Execution ───────────────────────────

# 1. AWS Lambda Handler
mcp_app = mcp.http_app()

async def asgi_wrapper(scope, receive, send):
    """Simple ASGI wrapper to show a message on the root path without using Starlette routes."""
    if scope["type"] == "http" and scope["path"] == "/":
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"This RAG Engine's MCP Server is Deployed in AWS Lambda.",
        })
        return
    # Pass all other requests (like /mcp) to the actual FastMCP app
    await mcp_app(scope, receive, send)

# Mangum wraps the ASGI app for Lambda
handler = Mangum(asgi_wrapper)

# 2. Local Executor (This only runs when you start it manually on your PC)
if __name__ == "__main__":
    import uvicorn
    print(f"Starting MCP Modular Server (HTTP) on http://{settings.mcp_host}:{settings.mcp_port}")
    # We run the wrapper with uvicorn so localhost:8000 also shows the message
    uvicorn.run(asgi_wrapper, host=settings.mcp_host, port=settings.mcp_port)
