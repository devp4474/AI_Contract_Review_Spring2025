# AI Contract Review — Spring 2025

This project is a desktop application that uses AI (LegalBERT) to analyze PDF and DOCX contracts for potentially risky legal language. The application highlights problematic clauses and provides AI-generated suggestions for improved phrasing.

---

## Features
- Upload any PDF or DOCX contract.
- AI scans and flags risky clauses using legal keywords and context.
- Suggestions are generated using LegalBERT.
- Annotated document is exportable as a new Word file with highlights and notes.
- Bundled as a macOS `.app` for ease of use (no coding required).

---

## How to Use

### Option 1: Run the Pre-Built macOS App
1. Download the `.zip` file from the GitHub [Releases](https://github.com/devp4474/AI_Contract_Review_Spring2025/releases).
2. Unzip it and open `ContractReviewApp.app`.
3. Click "Upload Contract" and select a `.docx` or `.pdf`.
4. After analysis, click "Export Annotated Version" to save your results.

### Option 2: Run from Source (for developers)

#### Requirements
- Python 3.10+
- [Poetry](https://python-poetry.org/) or `pip`
- macOS or Windows
- Internet connection to download models from Hugging Face

#### Install dependencies:
```bash
pip install -r requirements.txt

#### Run the app:
python src/gui.py

## Author
Dev Patel - Spring 2025
