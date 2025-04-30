# AI Contract Review — Spring 2025

This desktop application uses AI (LegalBERT) to analyze PDF and DOCX contracts for potentially risky legal language. It highlights problematic clauses and provides AI-generated suggestions for improved clarity and legal safety.

---

## Features

- Upload any PDF or DOCX contract.
- AI scans and flags risky clauses using legal keywords and contextual analysis.
- Suggestions are generated using LegalBERT.
- Annotated document can be exported as a new Word file with highlights and AI notes.
- Bundled as a macOS `.app` for easy use without any setup or coding.

---

## How to Use

### Option 1: Run the Pre-Built macOS App

1. [Download the `.zip` file from GitHub Releases](https://github.com/devp4474/AI_Contract_Review_Spring2025/releases).
2. Unzip the file and open `ContractReviewApp.app`.
3. Click "Upload Contract" and select a `.docx` or `.pdf` file.
4. Review the AI feedback in the interface.
5. Click "Export Annotated Version" to save the highlighted contract with notes.

### Option 2: Run from Source (Developer Mode)

#### Requirements

- Python 3.10+
- `pip` or [Poetry](https://python-poetry.org/)
- macOS or Windows
- Internet connection (used to download AI models from Hugging Face)

#### Install dependencies

```bash
pip install -r requirements.txt
