import streamlit as st
from HealthReportAnalyzer import HealthReportAnalyzer

st.title("Health report Q&A")

rep_analyzer = HealthReportAnalyzer(streamlit=True).run()

question = st.text_input("Question:")
st.write(rep_analyzer.llm_helper.ask_question(question))

