import util.DocUtil as util
from VectorStore import VectorStore
from LLMHelper import LLMHelper
from prompts import doctor_prompt, doctor_prompt_m

class HealthReportAnalyzer:
    
    def __init__(self, streamlit=False) -> None:
        self.model = "groq" # Change LLM model here - ollama, groq, openai, huggingface
        self.store: VectorStore = None
        self.streamlit = streamlit
        pass

    def run(self):
        path = './files/health-reports'
        
        if self.load_report(path):
            if self.streamlit:
                return self
            self.start_qna()

    def load_report(self, path):
        doc_chunks = util.doc_to_chunks(path)
        self.store = VectorStore(doc_chunks, self.model)
        self.llm_helper = LLMHelper(doctor_prompt_m, self.store, self.model)
        return True

    def start_qna(self):
        while True:
            ques = input("\nQuestion: ")
            if ques == 'exit':
                break
            else:
                self.llm_query(ques)

    def llm_query(self, ques):
        for chunk in self.llm_helper.ask_question(ques):
            if 'answer' in chunk:
                print(chunk['answer'], end="", flush=True)
        # print("\nAnswer: ", self.llm_helper.ask_question(ques))
