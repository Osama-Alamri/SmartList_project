import streamlit as st

st.title("SmartList")
"\n"
"\n"
"\n"

def add_big_task(title):
    with Rcont:
        with st.expander(title):
            st.checkbox(title)
LCol, RCol = st.columns(2)

with RCol:
    Rcont = st.container()
    with Rcont:
        Rcont.header("Tasks")
        task_textbox = st.text_input("Enter task: " )
        if st.button("Add task"):
            add_big_task(task_textbox)

   
    
with LCol:
    Lcont = st.container()
    with Lcont:
        Lcont.header("Ai Assessmint")

"\n"
"\n"
"\n"
st.write("out side line")

    # task_textbox = st.text_input("Enter big task: ")
    # if st.button("Add Big task"):
    #     if task_textbox:
    #         st.session_state["TaskList"] = []
         