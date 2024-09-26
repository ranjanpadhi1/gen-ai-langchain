from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

template = ChatPromptTemplate([
    ("system", "Translate given message in {language}"),
    ("user", "{message}")  
])

llm = ChatGroq(model="Gemma2-9b-It")
parser = StrOutputParser()

chain = template | llm | parser

# print(chain.invoke({"language": "Hindi", "message": "Hi, How are you?"}))

app = FastAPI(title="Language Translator", version="1.0")

add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)