# pdf_processor.py

from PyPDF2 import PdfReader

class PDFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_text(self):
        pdf_reader = PdfReader(self.file_path)
        raw_text = ''
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                raw_text += content
        return raw_text
