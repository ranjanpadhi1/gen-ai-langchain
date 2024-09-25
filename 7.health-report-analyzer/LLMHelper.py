from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.llms.ollama import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from VectorStore import VectorStore

class LLMHelper:

    def __init__(self, prompt_template, store: VectorStore, model) -> None:
        self.prompt_template = prompt_template
        self.store = store
        self.initialize(model)
        pass

    def initialize(self, model):
        template = ChatPromptTemplate.from_template(self.prompt_template)
        llm = self.create_llm(model)
        doc_chain = create_stuff_documents_chain(llm, template)

        retriever = self.store.get_db().as_retriever()
        self.r_chain = create_retrieval_chain(retriever, doc_chain)

    def create_llm(self, model):
        if model.lower() == "openai":
            return ChatOpenAI(model="gpt-4o")
        elif model.lower() == "ollama":
            return Ollama(model="gemma2:2b")
        
    def ask_question(self, question):
        return self.r_chain.invoke({"input": question})['answer']
    
    


