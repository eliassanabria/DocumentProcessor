import json
from app.gemini_client import GeminiClient
from app.rag.store import ChunkRecord


def create_issue_payload(
    client: GeminiClient,
    user_request: str,
    chunks: list[ChunkRecord]
) -> str:
    if not chunks:
        return "No relevant content found for issue creation."

    context = "\n\n".join([f"{chunk.chunk_id}:\n{chunk.text}" for chunk in chunks])

    prompt = f"""
You are creating a mock issue/ticket payload based ONLY on the document context.

User request:
{user_request}

Context:
{context}

Return valid JSON with this schema:
{{
  "title": "string",
  "priority": "Low | Medium | High",
  "summary": "string",
  "acceptance_criteria": ["string", "string"],
  "citations": ["chunk-1"]
}}
"""

    response = client.model.generate_content(prompt)
    raw_text = response.text.strip()

    try:
        parsed = json.loads(raw_text)
        return json.dumps(parsed, indent=2)
    except json.JSONDecodeError:
        return raw_text