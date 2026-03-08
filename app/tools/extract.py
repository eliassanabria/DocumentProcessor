from app.gemini_client import GeminiClient
from app.rag.store import ChunkRecord


def extract_requirements(client: GeminiClient, chunks: list[ChunkRecord]) -> str:
    if not chunks:
        return "No relevant content found for requirement extraction."

    context = "\n\n".join([f"{chunk.chunk_id}:\n{chunk.text}" for chunk in chunks])

    prompt = f"""
You are extracting actionable requirements from a document.

Using ONLY the context below, extract:
- requirement
- deadline (if any)
- owner (if any)
- source chunk id

Return as clean bullet points.

Context:
{context}
"""

    response = client.model.generate_content(prompt)
    return response.text.strip()