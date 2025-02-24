import openai
from dotenv import load_dotenv
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
load_dotenv()

# Azure AI Form Recognizer Credentials
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

# Azure OpenAI Credentials
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")

def get_form_recognizer_client():
    """Authenticate with Azure AI Form Recognizer."""
    return DocumentAnalysisClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))

def extract_text_from_pdf_or_docx(file_path):
    """Extract text from a PDF or DOCX file using Azure AI Form Recognizer."""
    client = get_form_recognizer_client()
    with open(file_path, "rb") as file:
        poller = client.begin_analyze_document("prebuilt-read", file)
        result = poller.result()
    extracted_text = "\n".join([line.content for page in result.pages for line in page.lines])
    return extracted_text.strip()

def analyze_contract_with_gpt(contract_text):
    """Analyze a contract's text using Azure OpenAI GPT-4 (New API)."""
    client = openai.AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint=AZURE_OPENAI_ENDPOINT
    )

    prompt = f"""Analyze the following contract and highlight any risky clauses related to liability, indemnification, termination, penalties, or warranties:
    
    {contract_text}

    Provide a detailed risk assessment.
    """

    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a legal contract analyst AI."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content  # Fix the response format
