# 🧬 Agentic RAG Microservice Engine
> **Distributed AI Reasoning & Cloud-Scale Vector Intelligence**

![UI Preview](./screenshots/UI%20of%20the%20RAG%20Engine.png)

---

## 🏗️ The "How It Works" Flow (Simplified)
Here’s the journey of a question in the **Agentic RAG Engine**:

```mermaid
flowchart TD
    User([👤 <b>You</b>]) -- "Ask a Question" --> UI[💻 <b>React UI</b>]
    UI -- "FastAPI Trigger" --> Brain[🧠 <b>AI Brain (LangGraph)</b>]
    
    subgraph Reasoning ["The Reasoning Loop"]
        Brain -- "Needs Facts?" --> ToolGate{<b>Decider</b>}
        ToolGate -- "YES" --> ToolCall[🛠️ <b>MCP Microservice</b>]
        ToolCall -- "Search Data" --> Database[(🗄️ <b>PGVector Memory</b>)]
        Database -- "Return Facts" --> ToolCall
        ToolCall -- "Inject Context" --> Brain
    end
    
    Brain -- "Final Answer" --> UI
    UI -- "Show Response" --> User
```

---

## 🧪 Experience the Power (Visual Showcase)
### **1. Intelligent Reasoning & Ingestion**
The AI doesn't just search—it understands. Here is the **Agentic Loop** in action, extracting contact details from a resume while keeping the conversation concise and professional.
![AI Output](./screenshots/Resume%20Uploaded%20and%20tested.png)

---

### **2. Cloud Infrastructure & Distributed Deployment**
This architecture is born in the cloud. We utilize **AWS ECR** for registry management, **AWS ECS/Lambda** for compute orchestration, and **AWS ELB** for traffic management.

| AWS Infrastructure | Operational Context |
| :--- | :--- |
| ![ECR](./screenshots/Docker%20Image%20stored%20in%20ECR.png) | **AWS ECR:** Securely hosting immutable Docker images for the RAG engine. |
| ![ECS](./screenshots/ECS%20Services.png) | **AWS ECS:** Orchestrating high-availability clusters for the AI Reasoning core. |
| ![ALB](./screenshots/Target%20Group%20and%20ALB.png) | **AWS Load Balancer (ALB):** Managing traffic routing and high-performance throughput. |
| ![Lambda](./screenshots/MCP%20Server%20Deployed%20in%20AWS%20Lambda.png) | **AWS Lambda:** Serverless microservice tools for infinite scaling on demand. |

---

### **3. Production-Grade Memory (RDS)**
Instead of ephemeral local files, all embeddings are stored in **Amazon RDS (PostgreSQL)** with **PGVector**, providing the AI with a persistent, industrial-strength brain.
![RDS](./screenshots/RDS%20Database%20PostgreSQL.png)

---

## ⛓️ Key Architectural Strengths

### 🧠 **Autonomous Decision Making (LangGraph)**
The AI observes your question, inspects its **Tools Manifesto**, and decides its own execution plan. If its first search is insufficient, it re-queries with more specific parameters—this is the true power of an "Agentic" loop.

### 🛰️ **Decoupled Microservice Tools (MCP)**
By using the **Model Context Protocol (MCP)** over HTTP, the "Tools" are completely decentralized. They can live independently as Docker containers or Serverless Lambda functions, making the system highly modular and easy to extend.

### 🧹 **Self-Cleaning Data Pipeline**
Ingestion happens in a secure environment. PDFs are vectorized and the local files are **instantly deleted** after ingestion, ensuring data security and a zero-waste local workspace.

---

## 🛠️ Tech Stack
- **AI/LLM:** LangGraph, Groq (Llama-3.1-8b)
- **Backend:** FastAPI (Microservices), Python 3.11
- **Database:** PostgreSQL **PGVector** (Vector Search)
- **Web:** React, Tailwind CSS
- **Cloud/Ops:** Docker, AWS (ECR, ECS, ELB, Lambda/Mangum, RDS)

---

## 🚀 Quick Setup

```bash
# 1. Start the Tool Microservice
python -m RAG.apps.mcp.server

# 2. Start the AI Engine
uvicorn RAG.apps.fastapi.main:app --reload --port 8001

# 3. Launch UI
cd RAG/apps/frontend && npm run dev
```

---

**Engineered for Distributed AI Excellence.** 🏁🏆🚩
