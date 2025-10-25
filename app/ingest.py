from pathlib import Path
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
import docx

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = ""
    for page in doc:
        t = page.get_text()
        if t and t.strip():
            text += t + "\n"
        else:
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes()))
            ocr = pytesseract.image_to_string(img, lang='eng+por')
            text += ocr + "\n"
    return text

def extract_text_from_docx(path: str) -> str:
    doc = docx.Document(path)
    full = []
    for p in doc.paragraphs:
        full.append(p.text)
    return "\n".join(full)

def extract_text_from_file(path: str) -> str:
    p = Path(path)
    suf = p.suffix.lower()
    if suf in ['.pdf']:
        return extract_text_from_pdf(path)
    if suf in ['.docx', '.doc']:
        return extract_text_from_docx(path)
    if suf in ['.txt']:
        return p.read_text(encoding='utf-8')
    if suf in ['.png', '.jpg', '.jpeg', '.tiff']:
        from PIL import Image
        img = Image.open(path)
        return pytesseract.image_to_string(img, lang='eng+por')
    raise ValueError('Unsupported file type')
