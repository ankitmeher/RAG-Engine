# --- STAGE 1: BUILDER ---
# We use the SAME AWS image as the builder! 
FROM public.ecr.aws/lambda/python:3.11 AS builder

# Install compilers available on Amazon Linux
RUN yum install -y gcc gcc-c++ postgresql-devel python3-devel && yum clean all

WORKDIR /build
COPY RAG/shared/requirements.txt ./shared-requirements.txt
COPY RAG/apps/mcp/requirements.txt ./mcp-requirements.txt

# Install into a local folder
# This will build Numpy FOR the Amazon Linux environment
RUN pip install --no-cache-dir --target=/build/deps \
    -r shared-requirements.txt \
    -r mcp-requirements.txt

# --- STAGE 2: FINAL ---
FROM public.ecr.aws/lambda/python:3.11

RUN yum install -y postgresql-libs && yum clean all

# Copy ONLY the pre-built dependencies from the Amazon-built stage
COPY --from=builder /build/deps ${LAMBDA_TASK_ROOT}/
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

CMD ["RAG.apps.mcp.server.handler"]
