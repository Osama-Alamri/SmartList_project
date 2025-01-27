import streamlit as st
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col2:
    st.title("To-Do List")

    if "task_list" not in st.session_state:
        st.session_state["task_list"] = []

    task = st.text_input("Enter your task", " ")

    if st.button("Add the task"):
        if task:
            st.session_state["task_list"].append(task)
            st.success("Task added!")
        else:
            st.warning("Please enter a task before adding.")

    for i , t in enumerate(st.session_state["task_list"]):
        if st.checkbox(f"{i+1}. {t}"):
            st.session_state["task_list"].remove(t)
            st.experimental_rerun()


with col1:
    st.header("AI Assistant")
    st.chat_input(placeholder="Your message")