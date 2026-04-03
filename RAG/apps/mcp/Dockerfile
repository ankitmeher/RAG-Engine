# ─── STAGE 1: BUILDER ───
# We use Python 3.11-slim which has modern compilers (GCC 12+)
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install all requirements into a temporary folder
WORKDIR /install
COPY RAG/shared/requirements.txt .
COPY RAG/apps/mcp/requirements.txt .

# We install everything to /install/lib to keep it separate
RUN pip install --no-cache-dir --prefix=/install \
    -r requirements.txt \
    -r shared/requirements.txt || \
    pip install --no-cache-dir --prefix=/install \
    -r requirements.txt \
    -r shared-reqs.txt # Fallback for path variations

# ─── STAGE 2: FINAL LAMBDA IMAGE ───
FROM public.ecr.aws/lambda/python:3.11

# Install runtime dependencies ONLY (much faster)
RUN yum install -y postgresql-libs && yum clean all

# Copy the pre-built packages from the builder stage
# This bypasses the need for GCC entirely in the Lambda image!
COPY --from=builder /install/lib/python3.11/site-packages ${LAMBDA_TASK_ROOT}/

# Copy your actual RAG code
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# Set the handler
CMD ["RAG.apps.mcp.server.handler"]
