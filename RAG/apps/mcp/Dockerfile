FROM python:3.11-slim

WORKDIR /app
# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 1. Install shared requirements
COPY RAG/shared/requirements.txt ./shared-reqs.txt
RUN pip install --no-cache-dir -r shared-reqs.txt

# 2. Install MCP specific requirements
COPY RAG/apps/mcp/requirements.txt ./app-reqs.txt
RUN pip install --no-cache-dir -r app-reqs.txt

# 3. Securely copy ONLY the backend Monorepo logic (Ignoring frontend UI & Node Modules)
COPY RAG/shared/ ./RAG/shared/
COPY RAG/apps/mcp/ ./RAG/apps/mcp/

# Expose SSE stream port
EXPOSE 8000

CMD ["python", "-m", "RAG.apps.mcp.server"]
