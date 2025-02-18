import pdfplumber
from docx import Document
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text.strip()

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def save_output(text, output_file):
    """Save extracted text to a file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":
    # Sample test files
    pdf_file = "data/sample.pdf"
    docx_file = "data/sample.docx"

    # Create output directory if not exists
    os.makedirs("output", exist_ok=True)

    # Process PDF
    try:
        pdf_text = extract_text_from_pdf(pdf_file)
        print("\n--- Extracted PDF Text ---\n", pdf_text[:500])  # Preview first 500 chars
        save_output(pdf_text, "output/scanned_pdf.txt")
        print(f"\n✅ PDF text saved to output/scanned_pdf.txt")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")

    # Process DOCX
    try:
        docx_text = extract_text_from_docx(docx_file)
        print("\n--- Extracted DOCX Text ---\n", docx_text[:500])  # Preview first 500 chars
        save_output(docx_text, "output/scanned_docx.txt")
        print(f"\n✅ DOCX text saved to output/scanned_docx.txt")
    except Exception as e:
        print(f"❌ Error reading DOCX: {e}")
