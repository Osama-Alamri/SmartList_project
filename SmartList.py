import streamlit as st
#pip3 install -U openai
#pip install requests
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

LCol , MCol , RCol = st.columns([3,1,3])

with LCol:
    st.title("ChatBot")

    if "messages" not in st.session_state:
        st.session_state.messages = []


    chat_container = st.container(border=True, height= 600)

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    prompt = st.chat_input("enter a message")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        
        response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

with MCol:
    st.title(" ")

with RCol:
    st.title("To-Do List")

    toDo_container = st.container(border=False, height = 900)
    with toDo_container:
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

    


# "\n"
# "\n"
# "\n"
# st.write("out side 1")

         