from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from VectorStore import VectorStore

class LLMHelper:

    def __init__(self, prompt_template, store: VectorStore) -> None:
        self.prompt_template = prompt_template
        self.store = store
        self.initialize()
        pass

    def initialize(self):
        template = ChatPromptTemplate.from_template(self.prompt_template)
        llm = ChatOpenAI(model="gpt-4o")
        doc_chain = create_stuff_documents_chain(llm, template)

        retriever = self.store.get_db().as_retriever()
        self.r_chain = create_retrieval_chain(retriever, doc_chain)

    def ask_question(self, question):
        return self.r_chain.invoke({"input": question})['answer']
    


