# chatbot.py

import os
import openai
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI
from slack_poster import SlackPoster
from dotenv import load_dotenv


class Chatbot:
    def __init__(self, raw_text, model="gpt-3.5-turbo"):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        self.model = model
        self.openai_api = OpenAI()
        self.text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)
        self.embeddings = OpenAIEmbeddings()
        self.document_search = None
        self.slack_poster = SlackPoster()

        # Load environment variables
        self.slack_token = os.getenv("SLACK_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")

        self.initialize_document_search(raw_text)

    def initialize_document_search(self, raw_text):
        texts = self.text_splitter.split_text(raw_text)
        self.document_search = FAISS.from_texts(texts, self.embeddings)

    def generate_response(self, messages):
        response = openai.ChatCompletion.create(model=self.model, messages=messages, max_tokens=150)
        return response

    def inference(self, query):
        docs = self.document_search.similarity_search(query)
        messages = [{"role": "system", "content": "You are a friendly chatbot and assistant"},
                    {"role": "user", "content": f"Question: {query}\nDocument: {docs}\nAnswer:"}]
        response = self.generate_response(messages)
        answer = response['choices'][0]['message']['content']
        print(answer)
        if "slack" in query.lower() and "push" in query.lower():
            results_json = {"Question": f"{query}", "Answer": f"{answer}"}
            self.slack_poster.post_results(results_json, self.slack_token, self.channel_id)
        return answer
