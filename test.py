import streamlit as st

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.title("ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []


    chat_container = st.container(border=True, height= 500)
    prompt = st.chat_input("enter a message")

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt:
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

        
        response = f"Echo: {prompt}"
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
