import streamlit as st
from openai import OpenAI

#Initialize OpenAI client
client = OpenAI(api_key=open('token').read(), base_url="https://api.deepseek.com/")

st.title("ChatBot")

#Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

#Chat display container
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

#Chat input field
prompt = st.chat_input("Enter a message")
if prompt:
    # Add user message to the chat
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare messages for the AI request
    messages = [{"role": message["role"], "content": message["content"]} for message in st.session_state.messages]

    # Send request to the AI model
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )

    # Collect the response
    reasoning_content = ""
    content = ""
    for chunk in response:
        if chunk.choices[0].delta.reasoning_content:
            reasoning_content += chunk.choices[0].delta.reasoning_content
        else:
            content += chunk.choices[0].delta.content

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(content)

    # Add assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": content})