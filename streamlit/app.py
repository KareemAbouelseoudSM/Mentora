import streamlit as st
from backend_requests import chat
import uuid
from helper_functions import stream
st.title("Mentora")

# Initialize session_id and user_id if not present
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Button to reset session and message history
if st.button("Reset Session"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(stream(chat(prompt, st.session_state.session_id, st.session_state.user_id)))
        st.session_state.messages.append({"role": "assistant", "content": response})

