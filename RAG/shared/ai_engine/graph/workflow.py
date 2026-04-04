"""
LangGraph workflow — compiles once and is reused for all requests.
Dynamic reasoning loop: agent decides if it needs tools.
"""

from functools import lru_cache

from langgraph.graph import END, StateGraph

from RAG.shared.ai_engine.graph.nodes import agent_node, tool_node
from RAG.shared.ai_engine.graph.state import RAGState


def should_continue(state: RAGState):
    """Router: check for native tool calls OR our manual 'CALL: ' string."""
    last_msg = state["messages"][-1]
    
    # 1. Standard tool calls
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    
    # 2. Our manual CALL: format
    if isinstance(last_msg.content, str) and "CALL: " in last_msg.content:
        return "tools"
        
    return END


@lru_cache(maxsize=1)
def _compiled_graph():
    workflow = StateGraph(RAGState)
    
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    workflow.set_entry_point("agent")
    
    # Conditional edge: LLM decides if it needs to call a tool or finish
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "agent": "agent",  # Add a fallback just in case
            END: END
        }
    )
    
    # After tools run, go back to the agent to rethink
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()


async def run_rag_pipeline(session_id: str, question: str) -> str:
    """Execute the Agentic reasoning loop. Returns the final answer string."""
    graph = _compiled_graph()
    result = await graph.ainvoke({
        "session_id": session_id,
        "question": question,
        "context": "",
        "answer": "",
        "messages": []
    })
    
    # The final message from the AI contains the answer
    return result["messages"][-1].content
