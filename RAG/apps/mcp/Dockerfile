FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum install -y gcc postgresql-devel && yum clean all

# 1. Install shared requirements
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-reqs.txt

# 2. Install MCP specific requirements
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/app-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/app-reqs.txt

# 3. Copy the entire RAG monorepo
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# Expose SSE stream port
EXPOSE 8000

CMD ["python", "-m", "RAG.apps.mcp.server"]
