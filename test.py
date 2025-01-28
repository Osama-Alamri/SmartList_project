import streamlit as st
from openai import OpenAI
import time
import requests
import google.generativeai as genai

###############################################################################################

genai.configure(api_key=open("./gemini.txt").read())
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Explain how AI works")
print(response.text)
##############################################################################################

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.title("ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container(border=True, height=400)
    prompt = st.chat_input("Enter a message")
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            
            try:
                response = model.generate_content(prompt)
                assistant_reply = response.text

            except Exception as e:
                response = f"An error occurred: {str(e)}"


            with st.chat_message("assistant"):
                    word_by_word_output = st.empty()  # Placeholder for dynamic word updates
                    words = assistant_reply.split()
                    displayed_text = ""
                    for word in words:
                        displayed_text += word + " "
                        word_by_word_output.markdown(displayed_text)
                        time.sleep(0.1)

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

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
