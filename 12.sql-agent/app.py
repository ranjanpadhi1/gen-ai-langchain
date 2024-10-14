import streamlit as st
from pathlib import Path
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
from langchain_groq import ChatGroq
from langchain.callbacks import StreamlitCallbackHandler

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "message": "Hi, How can I help you today?"}]

st.set_page_config(page_title="Chat with SQL DB")
st.title("Chat with SQL DB")

db_type = st.selectbox("Select Database to Connect", ["", "SQLite3", "MySQL"])

@st.cache_resource(ttl="2h")
def create_sql_conn(db_type):
    if db_type == "SQLite3":
        dbfilepath=(Path(__file__).parent/"emp.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(engine=create_engine("sqlite:///", creator=creator))
    else:
        return SQLDatabase(create_engine("mysql://root:admin@localhost:3306/emp"))

def create_agent(db):
    llm = ChatGroq(model_name="Llama3-8b-8192", streaming=True)
    return create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


if db_type:
    db = create_sql_conn(db_type)
    st.success(f"Connected to {db_type}")
    # st.write(db.run("select * from emp"))
    agent = create_agent(db)

    if user_query := st.chat_input("Ask anything from database"):
        st.session_state.messages.append({"role": "user", "content": user_query})
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            streamlit_callback=StreamlitCallbackHandler(st.container())
            response=agent.run(user_query,callbacks=[streamlit_callback])
            st.session_state.messages.append({"role":"assistant","content":response})
            st.write(response)


