import streamlit as st
import time
import google.generativeai as genai

# Configure Streamlit
st.set_page_config(layout="wide")
st.title(":sparkles:SmartList:sparkles:")

# Configure GenAI
genai.configure(api_key=open("./gemini.txt").read())
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if "task_list" not in st.session_state:
    st.session_state["task_list"] = []

if "suptask_list" not in st.session_state:
    st.session_state["suptask_list"] = {}

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Functions
def add_task(task_title):
    if task_title:
        task = {"title": task_title, "duration": None, "subtasks": []}
        st.session_state["task_list"].append(task)
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")

def delete_task(task_title):
    st.session_state["task_list"] = [
        task for task in st.session_state["task_list"] if task["title"] != task_title
    ]
    if task_title in st.session_state["suptask_list"]:
        del st.session_state["suptask_list"][task_title]
    st.success(f"Task '{task_title}' deleted successfully.")

def add_sup_task(sup_task_title, task_title):
    if sup_task_title:
        for task in st.session_state["task_list"]:
            if task["title"] == task_title:
                task["subtasks"].append(sup_task_title)
        st.success(f"Sub-task '{sup_task_title}' added under '{task_title}'!")
    else:
        st.warning("Please enter a sub-task before adding.")

# Layout
LCol, _, RCol = st.columns([10, 1, 10])

# Left Column - Chatbot
with LCol:
    st.title("ChatBot")
    chat_container = st.container()
    prompt = st.chat_input("Enter a message")

    with chat_container:
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state["messages"].append({"role": "user", "content": prompt})

            try:
                # Pass task list for processing
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
                assistant_reply = f"An error occurred: {str(e)}"

            st.chat_message("assistant").markdown(assistant_reply)
            st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

# Right Column - To-Do List
with RCol:
    st.title("To-Do List")
    task_textbox = st.text_input("Enter task:")
    if st.button("Add Task"):
        add_task(task_textbox)

    for task in st.session_state["task_list"]:
        with st.expander(task["title"]):
            # Delete Task Button
            if st.button(f"Delete Task '{task['title']}'", key=f"delete_{task['title']}"):
                delete_task(task["title"])
                st.experimental_rerun()

            # Add Subtask
            sup_task_textbox = st.text_input(f"Enter a sub-task for {task['title']}", key=f"sup_task_{task['title']}")
            if st.button(f"Add Sub-task to {task['title']}", key=f"add_suptask_{task['title']}"):
                add_sup_task(sup_task_textbox, task["title"])

            # Display Subtasks
            if task["subtasks"]:
                st.write("Sub-tasks:")
                for subtask in task["subtasks"]:
                    st.checkbox(subtask, key=f"subtask_checkbox_{subtask}")
