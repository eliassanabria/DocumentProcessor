from app.gemini_client import GeminiClient
from app.rag.store import ChunkRecord


def generate_checklist(client: GeminiClient, chunks: list[ChunkRecord]) -> str:
    if not chunks:
        return "No relevant content found for checklist generation."

    context = "\n\n".join([f"{chunk.chunk_id}:\n{chunk.text}" for chunk in chunks])

    prompt = f"""
You are generating a practical checklist from a document.

Using ONLY the context below:
- create a step-by-step checklist
- include any deadlines if present
- cite chunk IDs for each checklist item

Context:
{context}
"""

    response = client.model.generate_content(prompt)
    return response.text.strip()