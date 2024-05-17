# app.py

import streamlit as st
from pdf_processor import PDFProcessor
from chatbot import Chatbot

def main():
    st.title("PDF Chatbot")

    # File uploader for PDF
    st.sidebar.header("Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

    # If PDF is uploaded, extract text and initialize chatbot
    if uploaded_file is not None:
        st.sidebar.success("PDF uploaded successfully!")
        pdf_processor = PDFProcessor(uploaded_file)
        raw_text = pdf_processor.extract_text()
        chatbot = Chatbot(raw_text)

        # Chatbot interaction
        st.header("Chatbot")
        query = st.text_input("Enter your question")
        if st.button("Ask"):
            answer = chatbot.inference(query)
            st.write("")
            st.markdown(f"<div style='font-size: 18px'>{answer}</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
