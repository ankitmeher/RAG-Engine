"""
MCP Server Entry Point over SSE transport.
Only relies on `fastmcp` and imports modular tools.
Deployable as an AWS Lambda via Docker or running natively.
"""

from fastmcp import FastMCP

from RAG.shared.config.config import settings

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

if __name__ == "__main__":
    print(
        f"Starting MCP Modular Server (SSE) on "
        f"http://{settings.mcp_host}:{settings.mcp_port}/sse"
    )
    print("Registered tools:", ", ".join([v.name for v in getattr(mcp, "_tools", mcp.get_tools() if hasattr(mcp, "get_tools") else mcp.__dict__.get("tools", {}))]))
    
    # Run the server with SSE transport
    mcp.run(transport="sse", host=settings.mcp_host, port=settings.mcp_port)
