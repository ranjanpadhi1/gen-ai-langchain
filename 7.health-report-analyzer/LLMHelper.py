from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.llms.ollama import Ollama
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from VectorStore import VectorStore

class LLMHelper:

    def __init__(self, prompt, store: VectorStore, model) -> None:
        self.prompt = prompt
        self.store = store
        self.initialize(model)
        pass

    def initialize(self, model):
        # template = ChatPromptTemplate.from_template(self.prompt)
        template = ChatPromptTemplate.from_messages([("system", self.prompt), ("user", "{input}")])
        llm = self.create_llm(model)
        doc_chain = create_stuff_documents_chain(llm, template)

        retriever = self.store.get_db().as_retriever()
        self.r_chain = create_retrieval_chain(retriever, doc_chain)

    def create_llm(self, model):
        if model.lower() == "openai":
            return ChatOpenAI(model="gpt-4o")
        elif model.lower() == "groq":
            return ChatGroq(model="llama-3.1-70b-versatile") #Gemma2-9b-It
        elif model.lower() == "ollama":
            return Ollama(model="gemma2:2b")
        elif model.lower() == "huggingface":
            return ChatHuggingFace(model="gpt2")
        
    def ask_question(self, question):
        return self.r_chain.invoke({"input": question})['answer']
    
    


