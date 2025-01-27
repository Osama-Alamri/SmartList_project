import streamlit as st

st.title("SmartList")
"\n"
"\n"
"\n"

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

LCol, RCol = st.columns(2)

with RCol:
    st.title("To-Do List")
    task_textbox = st.text_input("Enter task: " )
    if st.button("Add task"):
        add_task(task_textbox)
    st.write("Tasks: ")

    #expander
    for task in st.session_state["task_list"]:
        with st.expander(task):
            sup_task_textbox = st.text_input(f"Enter a sub-task for {task}")
            if st.button(f"Add Sup-task to {task}"):
                add_sup_task(sup_task_textbox, task)
        #sup-task down the expander
            st.checkbox(task)
            if task in st.session_state["suptask_list"]:
                for sup_task in st.session_state["suptask_list"][task]:
                    st.checkbox(sup_task)

    
with LCol:
    Lcont = st.container()
    with Lcont:
        Lcont.title("Ai Assessmint")

"\n"
"\n"
"\n"
st.write("out side 1")

         