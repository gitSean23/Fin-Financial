import streamlit as st
# import openai
from langchain.llms import VertexAI

st.title("Fin")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Let's get yo money up! Start by asking me the basics."}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
