import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("SmartList")

# Initialize session states
if "task_list" not in st.session_state:
    st.session_state["task_list"] = []

if "suptask_list" not in st.session_state:
    st.session_state["suptask_list"] = {}

if "task_timing" not in st.session_state:
    st.session_state["task_timing"] = {}  # Stores start and end datetime for tasks


# Functions
def add_sup_task(sup_task_title, task_title):
    if sup_task_title:
        if task_title not in st.session_state["suptask_list"]:
            st.session_state["suptask_list"][task_title] = []
        st.session_state["suptask_list"][task_title].append(sup_task_title)
        st.success(f"Sup-task {sup_task_title} added under {task_title}!")
    else:
        st.warning("Please enter a sup-task before adding.")


def add_task(task_title):
    if task_title:
        st.session_state["task_list"].append(task_title)
        st.session_state["task_timing"][task_title] = {"start": None, "end": None}
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")


def calculate_time_consumed(start, end):
    if start and end:
        time_difference = end - start
        return str(time_difference)
    return None


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

    to_do_container = st.container()
    with to_do_container:
        task_textbox = st.text_input("Enter task: ")
        if st.button("Add task"):
            add_task(task_textbox)

        st.write("Tasks:")
        for task in st.session_state["task_list"]:
            with st.expander(task):
                sup_task_textbox = st.text_input(f"Enter a sub-task for {task}")
                if st.button(f"Add Sup-task to {task}"):
                    add_sup_task(sup_task_textbox, task)

                # Time tracking inputs
                st.write("Task Timing:")
                start_time = st.date_input(f"Start date for {task}", key=f"start_date_{task}")
                start_hour = st.time_input(f"Start time for {task}", key=f"start_time_{task}")
                end_time = st.date_input(f"End date for {task}", key=f"end_date_{task}")
                end_hour = st.time_input(f"End time for {task}", key=f"end_time_{task}")

                if st.button(f"Save timing for {task}"):
                    start = datetime.combine(start_time, start_hour)
                    end = datetime.combine(end_time, end_hour)

                    if start <= end:
                        st.session_state["task_timing"][task]["start"] = start
                        st.session_state["task_timing"][task]["end"] = end
                        st.success("Timing saved!")
                    else:
                        st.error("End time must be after start time.")

                # Display time consumed
                timing = st.session_state["task_timing"].get(task, {})
                if timing["start"] and timing["end"]:
                    time_consumed = calculate_time_consumed(timing["start"], timing["end"])
                    st.write(f"Time Consumed: {time_consumed}")
