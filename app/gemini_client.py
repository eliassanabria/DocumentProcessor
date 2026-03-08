from typing import List

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.rag.store import ChunkRecord


class GeminiClient:
    def __init__(self) -> None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")

        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def answer_grounded_question(
        self,
        question: str,
        chunks: List[ChunkRecord]
    ) -> str:
        if not chunks:
            return "I could not find relevant information in the document."

        context_blocks = []
        for chunk in chunks:
            context_blocks.append(f"{chunk.chunk_id}:\n{chunk.text}")

        context = "\n\n".join(context_blocks)

        prompt = f"""
You are a document analysis assistant.

Answer the user's question using ONLY the context below.
Do not use outside knowledge.
If the answer is not supported by the context, say:
"Not found in the provided document."

Requirements:
1. Be concise but clear.
2. Cite supporting chunk IDs inline like [chunk-2].
3. If multiple chunks support the answer, cite each relevant chunk.
4. Do not invent facts.

Context:
{context}

User question:
{question}
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except ResourceExhausted as error:
            return (
                "Gemini API quota was exceeded or is unavailable for this project.\n"
                f"Details: {error}"
            )
        except Exception as error:
            return f"Unexpected Gemini error: {error}"