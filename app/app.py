import streamlit as st
import requests
import json

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)
st.title("AI Assistant")

# Check if 'messages' are present in the session state, if not, initialize it as an empty list
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages stored in session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input and interact with the assistant
if prompt := st.chat_input("Message assistant..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Define API endpoint and data to be sent
        url = "http://agent:8000/chat"
        data = {"text": prompt}
        headers = {"Content-type": "application/json"}

        # Send request to the API
        with requests.post(url, data=json.dumps(data), headers=headers) as r:
            answer = r.json()

        # Display response from the assistant
        response = st.write(answer)

    # Add assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": answer})
