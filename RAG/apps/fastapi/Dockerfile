FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 1. Install shared requirements
COPY RAG/shared/requirements.txt ./shared-reqs.txt
RUN pip install --no-cache-dir -r shared-reqs.txt

# 2. Install FastAPI specific requirements
COPY RAG/apps/fastapi/requirements.txt ./app-reqs.txt
RUN pip install --no-cache-dir -r app-reqs.txt

# 3. Securely copy ONLY the backend Monorepo logic (Ignoring frontend UI & Node Modules)
COPY RAG/shared/ ./RAG/shared/
COPY RAG/apps/fastapi/ ./RAG/apps/fastapi/

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "RAG.apps.fastapi.main:app", "--host", "0.0.0.0", "--port", "8001"]
