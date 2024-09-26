import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
st.title("Language Translator")

text = st.text_area("Text", placeholder="Enter text to translate..")
language = st.selectbox("Choose Language", ["Hindi", "Telugu", "Odia", "French"])
btn = st.button("Translate")

if btn:
    prompt_template = ChatPromptTemplate([
        ("system", "Translate given text in ${language}"),
        ("user", "{text}")
    ])

    llm = ChatGroq(model="Gemma2-9b-It")
    parser = StrOutputParser()

    chain = prompt_template | llm | parser

    with st.container(border=True):
        st.write(chain.invoke({"language": language, "text": text}))

