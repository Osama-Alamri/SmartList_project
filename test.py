import streamlit as st
from openai import OpenAI
import time
import requests
import google.generativeai as genai
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import List, Optional
import json

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


class SubTask(BaseModel):
    """SubTask."""
    title: str = Field("list of a single word title of the SubTask")

class Task(BaseModel):
    """Task."""
    title: str = Field("a single word title of the Task")
    subtasks: List[SubTask] = []
    


    

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
    planer_text = st.text_area("I can plan your mission for you :wink:", key="planer_text", placeholder="e.g. I want to learn Python or manage my study plan")
    
    if st.button("Plan it :wink:", key="planer_buttom"):
        if planer_text:
            st.session_state.messages = []  # Clear previous chat history
            st.session_state.messages.append({"role": "user", "content": planer_text})

            try:
                # Updated prompt to request JSON output
                chatbot_prompt = f"""
                Here is the task: {planer_text}
                Please provide a response in **valid JSON format**.
                The response should contain a main task with at most 7 sub-tasks.
                Example format:
                {{
                    "title": "Main Task",
                    "subtasks": [
                        {{"title": "Subtask 1"}},
                        {{"title": "Subtask 2"}},
                        ...
                    ]
                }}
                Ensure that the response is **pure JSON only** without additional text.
                """

                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text.strip()

                # Debugging: Print response before parsing
                st.write("AI Response:", assistant_reply)

                # Ensure the response is not empty
                if not assistant_reply:
                    raise ValueError("Received an empty response from the AI model.")

                try:
                    # Attempt to parse the JSON response
                    assistant_tasks = json.loads(assistant_reply)

                    # Ensure at most 7 subtasks
                    if len(assistant_tasks.get("subtasks", [])) > 7:
                        assistant_tasks["subtasks"] = assistant_tasks["subtasks"][:7]

                    task = Task(**assistant_tasks)  # Convert to Pydantic model
                    st.session_state.messages.append({"role": "assistant", "content": json.dumps(assistant_tasks, indent=2)})

                except json.JSONDecodeError:
                    st.error("Error: AI response is not in valid JSON format. Please try again.")

            except Exception as e:
                st.error(f"Error generating mission plan: {e}")
        else:
            st.warning("Please provide a mission description.")

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