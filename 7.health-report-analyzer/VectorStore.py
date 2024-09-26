from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class VectorStore:
    
    def __init__(self, docs, model):
        self.db = None
        self.model = model
        self.initialize(docs)

    def initialize(self, docs):
        print(f"*** Using {self.model} Model ****")
        if self.model.lower() == "openai":
            embedding = OpenAIEmbeddings()
        if self.model.lower() == "groq":
            embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        elif self.model.lower() == "ollama":
            embedding = OllamaEmbeddings(model="mxbai-embed-large")
        elif self.model.lower() == "huggingface":
            embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
        self.db = FAISS.from_documents(docs, embedding)

    def get_db(self) -> FAISS:
        return self.db