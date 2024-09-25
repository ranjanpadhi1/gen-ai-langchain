from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

class VectorStore:
    
    def __init__(self, docs, model):
        self.db = None
        self.model = model
        self.initialize(docs)

    def initialize(self, docs):
        if self.model.lower() == "openai":
            embedding = OpenAIEmbeddings()
        elif self.model.lower() == "ollama":
            embedding = OllamaEmbeddings(model="mxbai-embed-large")
    
        self.db = FAISS.from_documents(docs, embedding)

    def get_db(self) -> FAISS:
        return self.db