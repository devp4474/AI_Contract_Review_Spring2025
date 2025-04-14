from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
)
import os
import shutil
import json
from pdf_docx_scanner import (
    extract_text_from_pdf_or_docx,
    analyze_contract_with_legalbert,
    create_annotated_contract
)

class ContractReviewApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Contract Review")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.upload_button = QPushButton("Upload Contract (PDF/DOCX)")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        self.file_label = QLabel("No file uploaded")
        self.layout.addWidget(self.file_label)

        self.preview_label = QLabel("Document Preview:")
        self.layout.addWidget(self.preview_label)
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.layout.addWidget(self.text_preview)

        self.analysis_label = QLabel("Flagged Clauses & AI Suggestions:")
        self.layout.addWidget(self.analysis_label)
        self.analysis_text = QTextEdit("Upload a contract to analyze.")
        self.analysis_text.setReadOnly(True)
        self.layout.addWidget(self.analysis_text)

        self.export_button = QPushButton("Export Annotated Version")
        self.export_button.clicked.connect(self.export_annotated_file)
        self.export_button.setEnabled(False)
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)
        self.uploaded_file_path = None
        self.export_file_path = None

    def upload_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Contract", "", "PDF Files (*.pdf);;Word Files (*.docx)")
            if not file_path:
                return

            self.uploaded_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"Uploaded: {file_name}")

            os.makedirs("output", exist_ok=True)
            self.export_file_path = os.path.join("output", f"annotated_{file_name.replace('.pdf', '.docx')}")

            print("🔍 Extracting text from contract...")
            extracted_text = extract_text_from_pdf_or_docx(file_path)
            if not extracted_text:
                self.analysis_text.setText("⚠️ Error extracting text from document.")
                return

            self.text_preview.setText(extracted_text[:1000])

            print("🤖 Analyzing contract with LegalBERT...")
            flagged_clauses = analyze_contract_with_legalbert(extracted_text)

            if not isinstance(flagged_clauses, dict):
                self.analysis_text.setText("⚠️ AI response error. Please try again.")
                return

            print("📄 Generating annotated contract...")
            create_annotated_contract(extracted_text, flagged_clauses, self.export_file_path)

            summary = "\n\n".join(
                f"• {c['original_text']}\n  → Suggestion: {c['suggestion']}"
                for c in flagged_clauses.get("flagged_clauses", [])
            )
            self.analysis_text.setText(summary or "✅ No major issues detected.")

            if os.path.exists(self.export_file_path):
                self.export_button.setEnabled(True)
            else:
                self.export_button.setEnabled(False)

            print(f"✏️ Flagged Clauses: {json.dumps(flagged_clauses, indent=2)}")

        except Exception as e:
            print(f"❌ Error processing file: {e}")
            self.analysis_text.setText(f"❌ Error: {e}")

    def export_annotated_file(self):
        if self.export_file_path and os.path.exists(self.export_file_path):
            default_filename = os.path.basename(self.export_file_path)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Annotated Contract", default_filename, "Word Files (*.docx)")
            if save_path:
                try:
                    shutil.copy(self.export_file_path, save_path)
                    print(f"✅ Annotated version saved to: {save_path}")
                    self.analysis_text.setText(f"✅ Annotated contract saved at: {save_path}")
                except Exception as e:
                    self.analysis_text.setText(f"❌ Error saving file: {e}")
        else:
            self.analysis_text.setText("⚠️ Error: Annotated file not found.")

if __name__ == "__main__":
    app = QApplication([])
    window = ContractReviewApp()
    window.show()
    app.exec_()
