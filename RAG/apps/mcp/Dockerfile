# AWS Lambda Python 3.12 = Amazon Linux 2023 (modern GCC 11+, GLIBC 2.34)
# This solves ALL numpy/scikit-learn/torch compilation errors
FROM public.ecr.aws/lambda/python:3.12

# Install system deps for psycopg2
RUN dnf install -y gcc postgresql-devel python3-devel && dnf clean all

# Upgrade pip
RUN pip install --upgrade pip --no-cache-dir

# Install shared requirements (langchain, sentence-transformers, etc.)
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-requirements.txt

# Install MCP requirements (fastmcp, mangum)
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/mcp-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/mcp-requirements.txt

# Copy main code
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# Set the Handler
CMD ["RAG.apps.mcp.server.handler"]
