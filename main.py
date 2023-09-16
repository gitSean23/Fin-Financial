# IF anything goes wrong and there is no explanation for it, it's prob the API KEY
import streamlit as st
import os
from api import apikey
os.environ["OPENAI_API_KEY"] = apikey
import openai


st.title("Fin")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Let's get yo money up! Start by asking me the basics."}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

    # openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)