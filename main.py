# IF anything goes wrong and there is no explanation for it, it's prob the API KEY
import streamlit as st
import os
from api import open_api_key
os.environ["OPENAI_API_KEY"] = open_api_key
import openai
from chain import create_qa_bot
from api import eleven_api_key
os.environ["ELEVEN_API_KEY"] = eleven_api_key
from elevenlabs import generate, play, set_api_key

set_api_key(eleven_api_key)

st.set_page_config(page_title="FinAI", page_icon="🐬")

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

    with st.spinner("Thinking.."):
        responseRole = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        responseRole1 = responseRole.choices[0].message
        response = create_qa_bot(prompt)
        newMsg = {"role": responseRole1["role"], "content": response}
        
        st.session_state.messages.append(newMsg)

        st.chat_message("assistant").write(newMsg["content"])
        
    audio = generate(
        text=response,
        voice="Bella",
        model="eleven_multilingual_v2",
        )

    play(audio)

