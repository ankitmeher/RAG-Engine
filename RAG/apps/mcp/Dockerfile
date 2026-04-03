# Use the official AWS Lambda Python 3.11 base image (Amazon Linux 2)
FROM public.ecr.aws/lambda/python:3.11

# AWS Lambda Python 3.11 uses Amazon Linux 2 (GLIBC 2.26).
# Numpy 2.0+ dropped pre-compiled wheels for this older Linux.
# By installing numpy<2 first, we force pip to use a pre-compiled binary,
# saving us from compiler errors and making the build 10x faster!
RUN pip install "numpy<2" --no-cache-dir

# Install shared requirements
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-requirements.txt

# Install MCP requirements
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/mcp-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/mcp-requirements.txt

# Copy main code
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# Set the Handler
CMD ["RAG.apps.mcp.server.handler"]

