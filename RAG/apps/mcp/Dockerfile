# ─── STAGE 1: BUILDER ───────────────────────────────────────────
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /install

# Copy both requirements with different names so they dont overwrite
COPY RAG/shared/requirements.txt     ./shared-requirements.txt
COPY RAG/apps/mcp/requirements.txt   ./mcp-requirements.txt

# Install both
RUN pip install --no-cache-dir --prefix=/install \
    -r mcp-requirements.txt \
    -r shared-requirements.txt

# ─── STAGE 2: LAMBDA IMAGE ──────────────────────────────────────
FROM public.ecr.aws/lambda/python:3.11

# Runtime dependency for psycopg2
RUN yum install -y postgresql-libs && yum clean all

# Copy pre-built packages from builder stage
COPY --from=builder /install/lib/python3.11/site-packages \
    ${LAMBDA_TASK_ROOT}/

# Copy RAG __init__.py so Python treats RAG as a package
COPY RAG/__init__.py ${LAMBDA_TASK_ROOT}/RAG/__init__.py

# Copy shared code (db_layer, ai_engine, config)
COPY RAG/shared/ ${LAMBDA_TASK_ROOT}/RAG/shared/

# Copy mcp app code (server.py, tools/, client.py)
COPY RAG/apps/mcp/ ${LAMBDA_TASK_ROOT}/RAG/apps/mcp/

# Lambda entry point
CMD ["RAG.apps.mcp.server.handler"]
