from pathlib import Path
from pypdf import PdfReader

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

def extract_pdf_text(data: bytes, filename: str) -> str:
    path = UPLOAD_DIR / filename.replace("/", "_").replace("\\", "_")
    path.write_bytes(data)
    reader = PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
