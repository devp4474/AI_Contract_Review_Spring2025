import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
)
from pdf_docx_scanner import extract_text_from_pdf, extract_text_from_docx

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

        # Placeholder analysis report
        self.analysis_label = QLabel("Analysis Report:")
        self.layout.addWidget(self.analysis_label)
        self.analysis_text = QTextEdit("Coming Soon!")
        self.analysis_text.setReadOnly(True)
        self.layout.addWidget(self.analysis_text)

        # Export button
        self.export_button = QPushButton("Export Annotated Version")
        self.export_button.clicked.connect(self.export_annotated_file)
        self.export_button.setEnabled(False)  # Initially disabled
        self.layout.addWidget(self.export_button)

        self.setLayout(self.layout)

        # Store uploaded file info
        self.uploaded_file_path = None
        self.export_file_path = None

    def upload_file(self):
        """Opens file dialog to select a PDF or DOCX file and previews its content."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Contract", "", "PDF Files (*.pdf);;Word Files (*.docx)")

        if file_path:
            self.uploaded_file_path = file_path
            file_name = os.path.basename(file_path)
            self.file_label.setText(f"Uploaded: {file_name}")

            # Ensure output directory exists
            os.makedirs("output", exist_ok=True)

            # Save a copy of the uploaded file
            self.export_file_path = os.path.join("output", file_name)
            shutil.copy(file_path, self.export_file_path)

            # Extract text and show preview
            if file_path.lower().endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_path)
            elif file_path.lower().endswith(".docx"):
                extracted_text = extract_text_from_docx(file_path)
            else:
                extracted_text = "Unsupported file format."

            self.text_preview.setText(extracted_text[:1000])  # Show only the first 1000 chars
            
            # Placeholder for analysis section (this will be AI-generated later)
            self.analysis_text.setText("Analysis Report: Coming Soon!")

            # Enable export button since a file is uploaded
            self.export_button.setEnabled(True)

    def export_annotated_file(self):
        """Exports the uploaded file as an 'annotated' copy (just a duplicate for now)."""
        if self.export_file_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Annotated Contract", self.export_file_path, "PDF Files (*.pdf);;Word Files (*.docx)")
            
            if save_path:
                shutil.copy(self.export_file_path, save_path)
                print(f"✅ Annotated version saved to {save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContractReviewApp()
    window.show()
    sys.exit(app.exec_())
