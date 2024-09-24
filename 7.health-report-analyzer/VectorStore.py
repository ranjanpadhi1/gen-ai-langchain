from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

class VectorStore:
    
    def __init__(self, docs):
        self.db = None
        self.initialize(docs)

    def initialize(self, docs):
        embedding = OpenAIEmbeddings()
        self.db = FAISS.from_documents(docs, embedding)

    def get_db(self) -> FAISS:
        return self.db