from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
)
import os
import shutil
from pdf_docx_scanner import extract_text_from_pdf_or_docx, analyze_contract_with_gpt

class ContractReviewApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Contract Review")
        self.setGeometry(100, 100, 800, 600)

        # Layout
        self.layout = QVBoxLayout()

        # Upload button
        self.upload_button = QPushButton("Upload Contract (PDF/DOCX)")
        self.upload_button.clicked.connect(self.upload_file)
        self.layout.addWidget(self.upload_button)

        # Display file name
        self.file_label = QLabel("No file uploaded")
        self.layout.addWidget(self.file_label)

        # Preview area
        self.preview_label = QLabel("Document Preview:")
        self.layout.addWidget(self.preview_label)
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.layout.addWidget(self.text_preview)

        # Analysis Report
        self.analysis_label = QLabel("Flagged Clauses:")
        self.layout.addWidget(self.analysis_label)
        self.analysis_text = QTextEdit("Upload a contract to analyze.")
        self.analysis_text.setReadOnly(True)
        self.layout.addWidget(self.analysis_text)

        # Export button
        self.export_button = QPushButton("Export Annotated Version")
        self.export_button.clicked.connect(self.export_annotated_file)
        self.export_button.setEnabled(False)
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)

        self.uploaded_file_path = None
        self.export_file_path = None

    def upload_file(self):
        """Uploads a contract and analyzes it using Azure OpenAI GPT-4."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Contract", "", "PDF Files (*.pdf);;Word Files (*.docx)")

            if not file_path:
                return  # If no file is selected, do nothing

            self.uploaded_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"Uploaded: {file_name}")

            os.makedirs("output", exist_ok=True)
            self.export_file_path = os.path.join("output", file_name)
            shutil.copy(file_path, self.export_file_path)

            # 🔹 Extract text using Azure AI
            extracted_text = extract_text_from_pdf_or_docx(file_path)
            self.text_preview.setText(extracted_text[:1000])  # Show first 1000 chars

            # 🔹 Use GPT-4 to analyze contract risks
            flagged_clauses = analyze_contract_with_gpt(extracted_text)
            self.analysis_text.setText(flagged_clauses if flagged_clauses else "No issues detected.")

            # Enable export button
            self.export_button.setEnabled(True)

        except Exception as e:
            print(f"❌ Error processing file: {e}")


    def export_annotated_file(self):
        """Exports the uploaded file (for now, just a copy)."""
        if self.export_file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Annotated Contract", self.export_file_path, "PDF Files (*.pdf);;Word Files (*.docx)")
            if save_path:
                shutil.copy(self.export_file_path, save_path)
                print(f"✅ Annotated version saved to {save_path}")

if __name__ == "__main__":
    app = QApplication([])
    window = ContractReviewApp()
    window.show()
    app.exec_()
