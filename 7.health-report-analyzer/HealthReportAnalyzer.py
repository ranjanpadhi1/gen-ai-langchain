import util.DocUtil as util
from VectorStore import VectorStore
from LLMHelper import LLMHelper
from prompts import health_report_prompt

class HealthReportAnalyzer:
    
    def __init__(self) -> None:
        self.store: VectorStore = None
        pass

    def run(self):
        path = './files/health-reports'
        
        if self.load_report(path):
            self.start_qna()

    def load_report(self, path):
        try:
            doc_chunks = util.doc_to_chunks(path)
            self.store = VectorStore(doc_chunks)
            self.llm_helper = LLMHelper(health_report_prompt, self.store)
            return True
        except:
            print('Error while processing the reports !')

    def start_qna(self):
        while True:
            ques = input("\nQuestion: ")
            if ques == 'exit':
                break
            else:
                self.llm_query(ques)

    def llm_query(self, ques):
        print("\nAnswer: ", self.llm_helper.ask_question(ques))
