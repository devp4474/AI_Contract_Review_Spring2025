import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from docx import Document
from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Load environment variables
load_dotenv()

# Get API keys
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Function to extract text from PDF or DOCX
def extract_text_from_pdf_or_docx(file_path):
    if file_path.endswith(".pdf"):
        client = DocumentAnalysisClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))
        with open(file_path, "rb") as file:
            poller = client.begin_analyze_document("prebuilt-read", file)
            result = poller.result()
        return "\n".join([line.content for page in result.pages for line in page.lines]).strip()
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]).strip()
    return ""

# Function to analyze contract using AI
def analyze_contract_with_gemini(contract_text):
    prompt = f"""
    You are a legal AI assistant. Analyze the following contract and:
    1. Identify problematic clauses related to liability, indemnification, termination, penalties, or warranties.
    2. Suggest alternative language for each flagged clause.
    3. Format your response as structured JSON:
    {{"flagged_clauses": [{{"original_text": "...", "issue": "...", "suggestion": "..."}}]}}
    Contract:
    {contract_text}
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    ai_response = response.text.strip()
    
    # Clean JSON artifacts
    ai_response = re.sub(r"```json|```", "", ai_response).strip()
    try:
        return json.loads(ai_response)
    except json.JSONDecodeError:
        return {"flagged_clauses": []}

# Function to add comments to Word doc
def add_comment(paragraph, comment_text):
    comment = OxmlElement("w:comment")
    comment.set(qn("w:author"), "AI Review")
    comment.set(qn("w:date"), "2025-03-10")
    comment.append(OxmlElement("w:p"))
    comment[0].text = comment_text
    paragraph._element.append(comment)

# Function to create an annotated contract
def create_annotated_contract(original_text, ai_output, output_path):
    doc = Document()
    doc.add_heading("Annotated Contract Review", level=1)
    
    paragraphs = original_text.split("\n\n")
    for para in paragraphs:
        flagged = next((c for c in ai_output.get("flagged_clauses", []) if c["original_text"] in para), None)
        
        p = doc.add_paragraph()
        run = p.add_run(para)
        
        if flagged:
            run.font.color = RGBColor(255, 0, 0)  # Highlight flagged text in red
            add_comment(p, f"Issue: {flagged['issue']}\nSuggestion: {flagged['suggestion']}")
        
    doc.save(output_path)