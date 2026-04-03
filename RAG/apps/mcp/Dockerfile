# 1. Use the official AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# 2. Install necessary system dependencies (gcc and postgres-devel for building psycopg2)
RUN yum install -y gcc postgresql-devel && yum clean all

# 3. Install shared requirements
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-reqs.txt

# 4. Install MCP specific requirements (Includes Mangum now!)
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/app-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/app-reqs.txt

# 5. Copy the RAG folder into the official Lambda task root
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# 6. Set the CMD to point to the Mangum handler inside your Python file
# Format: [filename].[function_name]
CMD ["RAG.apps.mcp.server.handler"]
