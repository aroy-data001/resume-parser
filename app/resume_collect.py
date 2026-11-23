from pypdf import PdfReader
from docx import Document

def resume(filepath):
    if filepath.suffix.lower() == ".pdf":
        return resumePDF(filepath)
    elif filepath.suffix.lower() == ".docx":
        return resumeDocx(filepath)
    else:
        return None

def resumePDF(filepath):
    text = ""
    reader = PdfReader(filepath)
    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def resumeDocx(filepath):
    text = ""
    reader = Document(filepath)
    for paragraph in reader.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"

    for table in reader.tables:
        for row in table.rows:
            for cell in row.cells:
                text += cell.text + "\n"

    return text
