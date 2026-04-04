"""
LangGraph nodes — Agentic RAG using MCP tools.
The LLM now 'decides' to call tools from the MCP server.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from RAG.shared.config.config import settings
from RAG.apps.mcp.client import RAGMCPClient
from RAG.shared.ai_engine.graph.state import RAGState


# ── LLM Setup ────────────────────────────────────────────────────────────────

def _get_llm():
    return ChatGroq(
        model=settings.groq_model,
        temperature=0,
        api_key=settings.groq_api_key,
    )


# ── MCP Tools (Available to the LLM) ──────────────────────────────────────────

@tool
async def search_vector_store(query: str):
    """
    Search the PDF document for relevant information. 
    Use this for ANY question where you need to look up facts from the uploaded file.
    Provide a clear, natural-language search query.
    """
    # This is a stub; actual execution happens in tool_node
    return "Searching..."


# ── Node 1: The Brain (Agent) ────────────────────────────────────────────────

import json
from pathlib import Path

async def agent_node(state: RAGState) -> dict:
    """The AI reads the manifest, understands its tools, and decides its next move."""
    llm = _get_llm()
    
    # Load manifest
    manifest_path = Path(__file__).parent.parent.parent.parent / "shared" / "ai_engine" / "tools_manifest.json"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    tools_desc = json.dumps(manifest["tools"], indent=2)

    # 1. ALWAYS start with the System Rules
    sys_msg = SystemMessage(content=(
        "You are a PDF Research Assistant. Rules:\n"
        "1. Be direct and concise, but provide ALL relevant details found in the context.\n"
        "2. Do NOT explain your process or mention 'based on context'.\n"
        "3. Respond ONLY with the factual answer.\n\n"
        f"Available Tools:\n{tools_desc}\n\n"
        "If info is missing, output: CALL: search_vector_store(query='...')\n"
    ))

    # 2. Handle conversation state
    if not state.get("messages"):
        # First time: System + User question
        initial_history = [HumanMessage(content=state["question"])]
        inputs = [sys_msg] + initial_history
        response = await llm.ainvoke(inputs)
        # Store both the question and the AI's first 'thought' (usually a CALL)
        return {"messages": initial_history + [response]}
    else:
        # Subsequent pass: SystemRules + History (which includes UserQ, AgentCALL, ContextResult)
        inputs = [sys_msg] + state["messages"]
        response = await llm.ainvoke(inputs)
        return {"messages": [response]}


# ── Node 2: Tool Execution (The Hands) ────────────────────────────────────────

import re

async def tool_node(state: RAGState) -> dict:
    """Execute tools and feed the result back as an internal knowledge update."""
    last_msg = state["messages"][-1]
    content = last_msg.content
    results = []
    
    # Flexible regex to catch any 'CALL: tool_name(arguments)'
    match = re.search(r"CALL:\s*(\w+)\((.*?)\)", content)
    
    if match:
        tool_name = match.group(1)
        args_str = match.group(2)
        
        print(f"--- [TOOL NODE] Executing {tool_name} ---")
        
        try:
            async with RAGMCPClient() as mcp:
                if tool_name == "search_vector_store":
                    # Parse query out of CALL: search_vector_store(query='...')
                    q_match = re.search(r"query=['\"](.*?)['\"]", args_str)
                    query = q_match.group(1) if q_match else state["question"]
                    chunks = await mcp.search_vector_store(state["session_id"], query)
                    out_text = "\n\n".join(chunks) if chunks else "No relevant context found."
                
                elif tool_name == "cleanup_session_data":
                    out_text = await mcp.cleanup_session(state["session_id"])
                
                else:
                    out_text = f"Tool '{tool_name}' exists in manifest but is not implemented in tool_node."

        except Exception as e:
            out_text = f"Error during tool execution: {e}"

        # FEEDBACK
        results.append(HumanMessage(content=(
            f"INTERNAL DATA RETRIEVED ({tool_name}):\n{out_text}\n\n"
            "Please provide a direct and complete answer using the data above."
        )))
            
    return {"messages": results}
