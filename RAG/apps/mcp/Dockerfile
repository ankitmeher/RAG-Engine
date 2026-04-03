# 1. Use the official AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# 2. Install EVERYTHING needed to build wheel files (Numpy, Sklearn, Psycopg2)
# We add 'gcc-c++' which was missing!
RUN yum install -y gcc gcc-c++ postgresql-devel python3-devel && yum clean all

# 3. Upgrade pip so it can find pre-built 'wheels' (saves time!)
RUN pip install --upgrade pip

# 4. Install shared requirements
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-reqs.txt

# 5. Install MCP specific requirements
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/app-reqs.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/app-reqs.txt

# 6. Copy the RAG folder
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# 7. Set the handler
CMD ["RAG.apps.mcp.server.handler"]
