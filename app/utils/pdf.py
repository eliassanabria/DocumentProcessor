from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from all pages in a PDF.
    """
    reader = PdfReader(pdf_path)
    all_text = []

    for page_index, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        if page_text.strip():
            all_text.append(f"[PAGE {page_index + 1}]\n{page_text}")

    return "\n\n".join(all_text)