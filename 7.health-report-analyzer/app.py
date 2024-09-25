import streamlit as st
from HealthReportAnalyzer import HealthReportAnalyzer

rep_analyzer = HealthReportAnalyzer(streamlit=True).run()
st.title("Virtual Doctor")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Start Conversation", key="user_input", placeholder="Type your message here and hit Enter ...")

if user_input:
    st.session_state.chat_history.append({"role": "human", "content": user_input})
    bot_response = rep_analyzer.llm_helper.ask_question(user_input)
    st.session_state.chat_history.append({"role": "ai", "content": bot_response})
    # st.session_state.user_input = ""

# with st.container(height=600, border=None):
for chat in st.session_state.chat_history:
    message = st.chat_message(chat["role"])
    message.write(chat["content"])
