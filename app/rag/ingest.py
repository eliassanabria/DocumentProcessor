from typing import List

from app.rag.store import ChunkRecord
from app.utils.pdf import extract_text_from_pdf
from app.utils.text import chunk_text


def ingest_pdf(pdf_path: str) -> List[ChunkRecord]:
    """
    Extracts and chunks a PDF into chunk records.
    """
    full_text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(full_text)

    records: List[ChunkRecord] = []
    for index, chunk in enumerate(chunks, start=1):
        records.append(
            ChunkRecord(
                chunk_id=f"chunk-{index}",
                text=chunk
            )
        )

    return records