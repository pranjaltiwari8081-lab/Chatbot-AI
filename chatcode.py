import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
load_dotenv() 
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
st.title("Chat with AI Made by Pranjal Tiwari")
if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            chat_history = "\n".join(
                [f"{'User' if m['role']=='user' else 'Gemini'}: {m['content']}" for m in st.session_state.messages]
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=chat_history
            )
            full_response = response.text
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.markdown(f"error: {e}")