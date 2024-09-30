import streamlit as st
from HealthReportAnalyzer import HealthReportAnalyzer
from dotenv import load_dotenv, dotenv_values
import time
load_dotenv()

rep_analyzer = HealthReportAnalyzer(streamlit=True).run()
st.set_page_config(page_title="Virtual Doctor")
st.title("Virtual Doctor")
st.text("Analyzes health report and provides recommendations")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

con = st.empty()

def chats():
    with con.container(height=600, border=0):
        for chat in st.session_state.chat_history:
            message = st.chat_message(chat["role"])
            message.write(chat["content"])
            
        global output_placeholder
        output_placeholder = st.empty()

chats()

def stream_fn(stream):
    global text
    text = ""
    for chunk in stream:
        if 'answer' in chunk:
            text += chunk['answer']
            yield chunk['answer']
            time.sleep(0.03)

if user_input := st.chat_input():
    st.session_state.chat_history.append({"role": "human", "content": user_input})
    chats()

    stream = rep_analyzer.llm_helper.ask_question(user_input)
    msg = output_placeholder.chat_message('ai')
    msg.write_stream(stream_fn(stream))

    bot_response = text
    text = ""
    output_placeholder.empty()
    st.session_state.user_input = ""
    
    st.session_state.chat_history.append({"role": "ai", "content": bot_response})
    chats()


    