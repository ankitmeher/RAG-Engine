"""
LangGraph workflow — compiles once and is reused for all requests.
"""

from functools import lru_cache

from langgraph.graph import END, StateGraph

from RAG.shared.ai_engine.graph.nodes import generate_node, retrieve_node
from RAG.shared.ai_engine.graph.state import RAGState


@lru_cache(maxsize=1)
def _compiled_graph():
    workflow = StateGraph(RAGState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate", generate_node)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    return workflow.compile()


def run_rag_pipeline(session_id: str, question: str) -> str:
    """Execute the retrieve → generate pipeline. Returns the answer string."""
    result = _compiled_graph().invoke({
        "session_id": session_id,
        "question": question,
        "context": "",
        "answer": "",
    })
    return result["answer"]
