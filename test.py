import streamlit as st
from openai import OpenAI

# Initialize the DeepSeek client
client = OpenAI(api_key=open("./token.txt").read().strip(), base_url="https://api.deepseek.com")

# Streamlit page configuration
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.title("ChatBot")

    # Initialize chat messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat container UI
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input prompt from user
    prompt = st.chat_input("Enter a message")

    if prompt:
        # Add user message to the session
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Make an API call to DeepSeek
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",  # Replace with your desired model name
                messages=st.session_state.messages,
                stream=False  # Use streaming if supported and desired
            )
            assistant_message = response['choices'][0]['message']['content']

        except Exception as e:
            assistant_message = f"Error: {str(e)}"

        # Add assistant response to the session and display it
        st.chat_message("assistant").markdown(assistant_message)
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

with col2:
    st.title("To-Do List")

    if "task_list" not in st.session_state:
        st.session_state["task_list"] = []

    task = st.text_input("Enter your task", "")

    if st.button("Add the task"):
        if task:
            st.session_state["task_list"].append(task)
            st.success("Task added!")
        else:
            st.warning("Please enter a task before adding.")

    for i , t in enumerate(st.session_state["task_list"]):
        if st.checkbox(f"{i+1}. {t}"):
            st.session_state["task_list"].remove(t)
