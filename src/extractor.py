import PyPDF2
from pathlib import Path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """
    Extracts text from a given PDF file using PyPDF2.
    
    Args:
        pdf_path: The path to the PDF file.
        
    Returns:
        A string containing the concatenated text from all pages.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")
        
    text_content = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(f"--- Page {page_num + 1} ---\n{page_text}")
                
    return "\n\n".join(text_content)
