from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Replace with your Azure details
AZURE_ENDPOINT = "your-endpoint-url-here"
AZURE_KEY = "your-api-key-here"

def test_azure_connection():
    """Check if Azure Document Intelligence API is working."""
    try:
        client = DocumentAnalysisClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))
        print("✅ Connected to Azure AI Document Intelligence successfully!")
    except Exception as e:
        print("❌ Failed to connect to Azure:", e)

if __name__ == "__main__":
    test_azure_connection()
