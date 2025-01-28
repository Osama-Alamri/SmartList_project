import streamlit as st
from openai import OpenAI
import time
import requests

###############################################################################################
client = OpenAI(
  api_key = open("./gpt_token.txt").read()
)


# print(completion.choices[0].message);

##############################################################################################

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

        
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=[
                    # {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            response = completion.choices[0].message.content
        except Exception as e:
            response = f"An error occurred: {str(e)}"


        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

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
