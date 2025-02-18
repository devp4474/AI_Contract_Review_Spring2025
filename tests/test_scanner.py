import os
import sys

# Add the 'src' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from pdf_docx_scanner import extract_text_from_pdf, extract_text_from_docx

def test_extract_text_from_pdf():
    """Test PDF text extraction."""
    pdf_path = "data/sample.pdf"
    if os.path.exists(pdf_path):
        text = extract_text_from_pdf(pdf_path)
        assert len(text) > 0  # Ensure some text is extracted

def test_extract_text_from_docx():
    """Test DOCX text extraction."""
    docx_path = "data/sample.docx"
    if os.path.exists(docx_path):
        text = extract_text_from_docx(docx_path)
        assert len(text) > 0  # Ensure some text is extracted
