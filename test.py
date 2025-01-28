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
    if "task_list" not in st.session_state:
        st.session_state["task_list"] = []

    if "suptask_list" not in st.session_state:
        st.session_state["suptask_list"] = {}

    def add_sup_task(sup_task_title, task_title):
        if sup_task_title:
            if task_title not in st.session_state["suptask_list"]:
                st.session_state["suptask_list"][task_title] = []
            st.session_state["suptask_list"][task_title].append(sup_task_title)
            st.success(f"Sup-task {sup_task_title} added under {task_title} !")
        else:
            st.warning("Please enter a sup-task before adding.")

    def add_task(task_title):
        if task_title:           
            st.session_state["task_list"].append(task_title)
            st.success("Task added!")
        else:
            st.warning("Please enter a task before adding.")
            
    def delete_task(task_title):
        st.session_state["task_list"].remove(task_title)
        st.success("delete this task success")
        st.title("To-Do List")

    to_do_container = st.container(border=False, height=900)

    with to_do_container:
        task_textbox = st.text_input("Enter task: ")
        if st.button("Add task"):
            add_task(task_textbox)
        st.write("Tasks: ")
 
        #expander
        for task in st.session_state["task_list"]:   
            with st.expander(task):
                if st.button("delete this task"):
                    delete_task(task)
                sup_task_textbox = st.text_input(f"Enter a sub-task for {task}") 
                if st.button(f"Add Sup-task to {task}"):
                    add_sup_task(sup_task_textbox, task) # add sup-task

                total_count = 0
                check_count = 0 

        # to make sup-task with exapnder
                for sup_task in st.session_state["suptask_list"][task]:
                    total_count += 1
                    if st.checkbox(sup_task):
                        check_count += 1
                # prograss line
                if total_count > 0:
                    progress = check_count / total_count
                    if progress == 1:
                        st.write("Excellent you finish this task !")
                        st.progress(progress)
                    else:
                        st.progress(progress)