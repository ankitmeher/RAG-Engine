# Use the official AWS Lambda Python 3.11 base image (Amazon Linux 2)
FROM public.ecr.aws/lambda/python:3.11

# Step 1: Upgrade pip, setuptools, wheel FIRST
# The default pip (24.0) is too old to find pre-built binary wheels
RUN pip install --upgrade pip setuptools wheel --no-cache-dir

# Step 2: Install system compilers for C-extensions (psycopg2, etc.)
RUN yum install -y gcc gcc-c++ postgresql-devel python3-devel && yum clean all

# Step 3: Pin numpy to 1.x (has pre-built wheels for Amazon Linux 2)
# Numpy 2.0+ requires GLIBC 2.27+ which Amazon Linux 2 does NOT have
RUN pip install "numpy<2" --no-cache-dir

# Step 4: Install shared requirements
COPY RAG/shared/requirements.txt ${LAMBDA_TASK_ROOT}/shared-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/shared-requirements.txt

# Step 5: Install MCP requirements
COPY RAG/apps/mcp/requirements.txt ${LAMBDA_TASK_ROOT}/mcp-requirements.txt
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/mcp-requirements.txt

# Step 6: Copy main code
COPY RAG/ ${LAMBDA_TASK_ROOT}/RAG/

# Step 7: Set the Handler
CMD ["RAG.apps.mcp.server.handler"]
