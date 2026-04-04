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
# Mangum wraps the FastMCP HTTP app for Lambda
handler = Mangum(mcp.http_app())

# 2. Local Executor (This only runs when you start it manually on your PC)
if __name__ == "__main__":
    print(f"Starting MCP Modular Server (HTTP) on http://{settings.mcp_host}:{settings.mcp_port}")
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)
