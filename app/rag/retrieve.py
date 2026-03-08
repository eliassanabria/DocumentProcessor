from typing import List

from app.rag.store import ChunkRecord, InMemoryVectorStore


def retrieve_relevant_chunks(
    store: InMemoryVectorStore,
    question: str,
    top_k: int = 4
) -> List[ChunkRecord]:
    return store.search(question, top_k=top_k)