import streamlit as st
from openai import OpenAI
import time
import requests
import google.generativeai as genai
from pydantic import BaseModel, Field
from pydantic_ai import Agent


st.set_page_config(layout="wide")
st.title(":sparkles:SmartList:sparkles:")
"\n"
"\n"

genai.configure(api_key=open("./gemini.txt").read())
model = genai.GenerativeModel("gemini-1.5-flash")

if "task_list" not in st.session_state:
    st.session_state["task_list"] = []

if "suptask_list" not in st.session_state:
    st.session_state["suptask_list"] = {}

if "messages" not in st.session_state:
    st.session_state.messages = []


def add_task(task_title):
    if task_title:
        task = {"title": task_title, "duration": None, "subtasks": []}           
        st.session_state["task_list"].append(task)
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")

def add_sup_task(sup_task_title, task_title):
    if sup_task_title:
        if task_title not in st.session_state["suptask_list"]:
            st.session_state["suptask_list"][task_title] = []
        st.session_state["suptask_list"][task_title].append(sup_task_title)
        st.success(f"Sup-task {sup_task_title} added under {task_title} !")
    else:
        st.warning("Please enter a sup-task before adding.")
        
def delete_task(task_title):
    st.session_state["task_list"] = [
        task for task in st.session_state["task_list"] if task["title"] != task_title
    ]
    if task_title in st.session_state["suptask_list"]:
        del st.session_state["suptask_list"][task_title]
    st.success(f"Task '{task_title}' deleted successfully.")


lm , mm , rm = st.columns([1,2,1])

with lm:
    st.write("")

with mm:
    st.text_area("I can plan your mission for you :wink:")
    if st.button("plan it 😉"):
        print("")
with lm:
    st.write("")


LCol , MCol , RCol = st.columns([10,1,10])

with LCol:
    st.title("ChatBot")

    chat_container = st.container(border=True, height=500)
    prompt = st.chat_input("Enter a message")
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt  :
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            
            try:
                task_data = "\n".join(
                    [
                        f"{idx + 1}. {task['title']} (Duration: {task.get('duration', 'N/A')})"
                        for idx, task in enumerate(st.session_state["task_list"])
                    ]
                )
                chatbot_prompt = (
                    f"Here are the tasks:\n{task_data}\n\nUser said: {prompt}\n"
                    "Please organize or respond based on these tasks."
                )
                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text

            except Exception as e:
                st.error(f"An error occurred while generating the response: {str(e)}")


            
            with st.chat_message("assistant"):
                    word_by_word_output = st.empty()  # Placeholder for dynamic word updates
                    words = assistant_reply.split()
                    displayed_text = ""
                    for word in words:
                        displayed_text += word + " "
                        word_by_word_output.markdown(displayed_text)
                        time.sleep(0.1)

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})


with MCol:
    st.title(" ")


with RCol:
    st.title("To-Do List")

    to_do_container = st.container(border=False, height=1500)
    with to_do_container:
        task_textbox = st.text_input("Enter task: ", key="task_input")
        if st.button("Add task"):
            add_task(st.session_state["task_input"])

        st.write("Tasks: ")
 
        #expander
        for task in st.session_state["task_list"]:   
            with st.expander(task["title"]):
                if st.button("delete this task", key=f"delete_{task['title']}"):
                    delete_task(task["title"])
                    st.experimental_rerun()

                sup_task_textbox = st.text_input(f"Enter a sub-task for {task['title']}") 
                if sup_task_textbox and st.button(f"Add Sup-task to {task['title']}", key=f"add_suptask_{task['title']}"):
                    add_sup_task(sup_task_textbox, task["title"]) 

                total_count = 0
                check_count = 0 
        
        # to make sup-task with exapnder
                for sup_task in st.session_state["suptask_list"].get(task["title"], []):
                    total_count += 1
                    if st.checkbox(sup_task):
                        check_count += 1
                # prograss line
                if total_count > 0:
                    progress = check_count / total_count
                    if progress == 1:
                        st.write("Excellent you finish this task !")
                        st.progress(progress)
                        st.write(f"{check_count} out of {total_count} subtasks completed.")
                    else:
                        st.progress(progress)