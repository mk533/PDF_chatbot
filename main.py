# main.py

from pdf_processor import PDFProcessor
from chatbot import Chatbot

def main():
    pdf_processor = PDFProcessor('handbook.pdf')
    raw_text = pdf_processor.extract_text()
    chatbot = Chatbot()
    chatbot.initialize_document_search(raw_text)

if __name__ == "__main__":
    main()
