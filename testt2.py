import streamlit as st

def initialize_state():
    """Initialize session state variables."""
    if "task_list" not in st.session_state:
        st.session_state["task_list"] = []

    if "suptask_list" not in st.session_state:
        st.session_state["suptask_list"] = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []

def add_sup_task(sup_task_title, task_title):
    """Add a sub-task to a specific task."""
    if sup_task_title:
        if task_title not in st.session_state["suptask_list"]:
            st.session_state["suptask_list"][task_title] = []
        st.session_state["suptask_list"][task_title].append(sup_task_title)
        st.success(f"Sup-task '{sup_task_title}' added under '{task_title}'!")
    else:
        st.warning("Please enter a sub-task before adding.")

def add_task(task_title):
    """Add a task to the task list."""
    if task_title:
        st.session_state["task_list"].append(task_title)
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")

def render_chatbot():
    """Render the chatbot UI in the left column."""
    st.title("ChatBot")
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

def render_todo_list():
    """Render the to-do list UI in the right column."""
    st.title("To-Do List")
    to_do_container = st.container()

    with to_do_container:
        task_textbox = st.text_input("Enter task: ")
        if st.button("Add task"):
            add_task(task_textbox)

        st.write("Tasks:")
        for task in st.session_state["task_list"]:
            with st.expander(task, expanded=True):
                sup_task_textbox = st.text_input(f"Enter a sub-task for {task}")
                if st.button(f"Add Sub-task to {task}"):
                    add_sup_task(sup_task_textbox, task)

                total_count = 0
                check_count = 0
                for sup_task in st.session_state["suptask_list"].get(task, []):
                    total_count += 1
                    if st.checkbox(sup_task):
                        check_count += 1

                if total_count > 0:
                    progress = check_count / total_count
                    if progress == 1:
                        st.write("Excellent! You finished this task!")
                    st.progress(progress)

def main():
    """Main function to render the app."""
    st.set_page_config(layout="wide")
    st.title("SmartList")
    initialize_state()

    LCol, MCol, RCol = st.columns([3, 1, 3])

    with LCol:
        render_chatbot()

    with MCol:
        st.title(" ")  # Empty middle column

    with RCol:
        render_todo_list()

if __name__ == "__main__":
    main()
