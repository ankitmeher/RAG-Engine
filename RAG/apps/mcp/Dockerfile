# --- STAGE 1: BUILDER ---
FROM python:3.11-slim AS builder

# We need these to build Psycopg2 and other C-extensions
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy requirements from the context (Root)
COPY RAG/shared/requirements.txt ./shared-requirements.txt
COPY RAG/apps/mcp/requirements.txt ./mcp-requirements.txt

# Install directly to a specific folder
RUN pip install --no-cache-dir --target=/build/deps \
    -r shared-requirements.txt \
    -r mcp-requirements.txt

# --- STAGE 2: FINAL ---
FROM public.ecr.aws/lambda/python:3.11

# Runtime library for Postgres
RUN yum install -y postgresql-libs && yum clean all

# 1. Copy the pre-built dependencies into the Lambda root
COPY --from=builder /build/deps ${LAMBDA_TASK_ROOT}/

# 2. Copy the code into the Lambda root
# We copy the entire RAG folder so imports like "from RAG.shared..." work
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# 3. Set the Handler
CMD ["RAG.apps.mcp.server.handler"]
