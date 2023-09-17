# IF anything goes wrong and there is no explanation for it, it's prob the API KEY
import streamlit as st
import os
from api import open_api_key
os.environ["OPENAI_API_KEY"] = open_api_key
import openai
from chain import create_qa_bot

st.set_page_config(page_title="FinAI", page_icon="🐬")

st.title("FinAI🐬")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I'm Fin! I'm here to help you take control of your finances, no matter your background. Let's work together to build a brighter financial future for you and your community. Ask me anything!"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

    # openai.api_key = openai_api_key

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking.."):
        responseRole = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        responseRole1 = responseRole.choices[0].message
        response = create_qa_bot(prompt)
        newMsg = {"role": responseRole1["role"], "content": response}
        
        st.session_state.messages.append(newMsg)

        st.chat_message("assistant").write(newMsg["content"])

    

