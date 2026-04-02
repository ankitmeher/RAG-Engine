from typing import List, TypedDict


class RAGState(TypedDict):
    session_id: str
    question: str
    context: str     # joined chunk texts passed to LLM
    answer: str
