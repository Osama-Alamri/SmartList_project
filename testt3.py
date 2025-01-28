import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide")
st.title("SmartList")
"\n"
"\n"

# Initialize session states
if "task_list" not in st.session_state:
    st.session_state["task_list"] = []  # List of tasks with details

if "suptask_list" not in st.session_state:
    st.session_state["suptask_list"] = {}  # Subtasks for tasks

# Functions
def add_big_task(task_title, order, start_time=None, end_time=None):
    if task_title and order is not None:
        task_data = {
            "title": task_title,
            "order": order,
            "start_time": start_time,
            "end_time": end_time,
        }
        st.session_state["task_list"].append(task_data)
        st.session_state["task_list"].sort(key=lambda x: x["order"])  # Sort by order
        st.success(f"Task '{task_title}' added successfully!")
    else:
        st.warning("Please fill in the task title and order.")

def delete_big_task(task_title):
    st.session_state["task_list"] = [task for task in st.session_state["task_list"] if task["title"] != task_title]
    st.session_state["suptask_list"].pop(task_title, None)
    st.success(f"Task '{task_title}' deleted successfully!")

def add_sup_task(sup_task_title, task_title):
    if sup_task_title:
        if task_title not in st.session_state["suptask_list"]:
            st.session_state["suptask_list"][task_title] = []
        st.session_state["suptask_list"][task_title].append(sup_task_title)
        st.success(f"Sub-task '{sup_task_title}' added under '{task_title}'!")
    else:
        st.warning("Please enter a sub-task before adding.")

def delete_sup_task(task_title, sup_task_title):
    if task_title in st.session_state["suptask_list"]:
        st.session_state["suptask_list"][task_title] = [
            sup_task for sup_task in st.session_state["suptask_list"][task_title] if sup_task != sup_task_title
        ]
        st.success(f"Sub-task '{sup_task_title}' deleted successfully!")

# Layout
LCol, MCol, RCol = st.columns([3, 1, 3])

# Chatbot Section
with LCol:
    st.title("ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Enter a message")

        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = f"Echo: {prompt}"
            with st.chat_message("assistant"):
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

# Spacer
with MCol:
    st.title(" ")

# To-Do List Section
with RCol:
    st.title("To-Do List")

    # Form to add a new big task
    with st.form("add_task_form"):
        task_title = st.text_input("Enter task title:")
        order = st.number_input("Task order (number):", min_value=1, step=1)
        include_time = st.checkbox("Add time to task?")
        start_time, end_time = None, None

        if include_time:
            start_date = st.date_input("Start date:")
            start_time = st.time_input("Start time:")
            end_date = st.date_input("End date:")
            end_time = st.time_input("End time:")
            start_time = datetime.combine(start_date, start_time)
            end_time = datetime.combine(end_date, end_time)

        submitted = st.form_submit_button("Add Big Task")
        if submitted:
            add_big_task(task_title, order, start_time, end_time)

    # Display tasks and subtasks
    st.write("Tasks:")
    for task in st.session_state["task_list"]:
        with st.expander(f"{task['order']}. {task['title']}"):
            # Display task details
            st.write(f"Start Time: {task['start_time']}" if task["start_time"] else "No start time")
            st.write(f"End Time: {task['end_time']}" if task["end_time"] else "No end time")

            # Delete task button
            if st.button(f"Delete Task '{task['title']}'"):
                delete_big_task(task["title"])

            # Add sub-task
            sup_task_textbox = st.text_input(f"Enter a sub-task for '{task['title']}'", key=f"sup_task_input_{task['title']}")
            if st.button(f"Add Sub-task to '{task['title']}'", key=f"add_sup_task_btn_{task['title']}"):
                add_sup_task(sup_task_textbox, task["title"])

            # Display sub-tasks
            total_count = 0
            check_count = 0
            for sup_task in st.session_state["suptask_list"].get(task["title"], []):
                total_count += 1
                col1, col2 = st.columns([6, 1])
                with col1:
                    if st.checkbox(sup_task, key=f"{task['title']}_{sup_task}"):
                        check_count += 1
                with col2:
                    if st.button(f"Delete '{sup_task}'", key=f"delete_sup_task_{task['title']}_{sup_task}"):
                        delete_sup_task(task["title"], sup_task)

            # Progress bar
            if total_count > 0:
                progress = check_count / total_count
                if progress == 1:
                    st.write("Excellent! You finished this task!")
                st.progress(progress)
