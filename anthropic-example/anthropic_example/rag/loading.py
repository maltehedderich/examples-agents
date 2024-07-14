from pathlib import Path

from pypdf import PdfReader


def load_pdf(path: Path) -> tuple[str, str]:
    reader = PdfReader(path)
    text = "\n".join([page.extract_text() for page in reader.pages])
    return text, path.name
