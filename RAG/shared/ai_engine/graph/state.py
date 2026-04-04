from typing import Annotated, List, TypedDict, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class RAGState(TypedDict):
    session_id: str
    question: str
    # Context is optionally populated by tools
    context: str
    answer: str
    # Messages track the conversation and tool calls/outputs
    messages: Annotated[List[BaseMessage], add_messages]
