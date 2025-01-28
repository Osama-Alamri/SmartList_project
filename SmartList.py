import streamlit as st
st.set_page_config(layout="wide")
st.title("SmartList")
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
        
def delete_task(task_title):
    st.session_state["task_list"].remove(task_title)
    st.success("delete this task success")

LCol , MCol , RCol = st.columns([3,1,3])

with LCol:
    st.title("ChatBot")


with MCol:
    st.title(" ")


with RCol:
    st.title("To-Do List")

    to_do_container = st.container(border=False, height=900)
    with to_do_container:
        task_textbox = st.text_input("Enter task: ")
        if st.button("Add task"):
            add_task(task_textbox)
        st.write("Tasks: ")
 
        #expander
        for task in st.session_state["task_list"]:   
            with st.expander(task):
                if st.button("delete this task"):
                    delete_task(task)
                sup_task_textbox = st.text_input(f"Enter a sub-task for {task}") 
                if st.button(f"Add Sup-task to {task}"):
                    add_sup_task(sup_task_textbox, task) # add sup-task

                total_count = 0
                check_count = 0 

        # to make sup-task with exapnder
                for sup_task in st.session_state["suptask_list"][task]:
                    total_count += 1
                    if st.checkbox(sup_task):
                        check_count += 1
                # prograss line
                if total_count > 0:
                    progress = check_count / total_count
                    if progress == 1:
                        st.write("Excellent you finish this task !")
                        st.progress(progress)
                    else:
                        st.progress(progress)
                    



# "\n"
# "\n"
# "\n"
# st.write("out side 1")