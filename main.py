import streamlit as st
import os
import openai
from elevenlabs import generate, play, set_api_key
from chain import create_qa_bot
from dotenv import load_dotenv

# openai_api_key = config('OPENAI_API_KEY')
# ELEVEN_API_KEY = config('ELEVEN_API_KEY')

load_dotenv()

openai_api_key = os.environ['OPENAI_API_KEY']
set_api_key(os.environ['ELEVEN_API_KEY'])

st.set_page_config(page_title="FinAI", page_icon="🐬")

st.title("FinAI 🐬")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello, I'm Fin! I'm here to help you take control of your finances, no matter your background. Let's work together to build a brighter financial future for you and your community. Ask me anything!"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner("Thinking.."):
        response = create_qa_bot(prompt)
        newMsg = {"role": "assistant", "content": response}
        
        st.session_state.messages.append(newMsg)

        st.chat_message("assistant").write(newMsg["content"])
        
    # audio = generate(
    #     text=response,
    #     voice="Bella",
    #     model="eleven_multilingual_v2"
    #     )

    # play(audio)

