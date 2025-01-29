import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(layout="wide")
st.title(":sparkles:SmartList:sparkles:")
"\n"
"\n"

genai.configure(api_key=open("./gemini.txt").read())
model = genai.GenerativeModel("gemini-1.5-flash")

if "task_list" not in st.session_state:
    st.session_state["task_list"] = []

if "subtask_list" not in st.session_state:
    st.session_state["subtask_list"] = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

def add_sub_task(subtask_list, task_title):
    if subtask_list:
        if task_title not in st.session_state["subtask_list"]:
            st.session_state["subtask_list"][task_title] = []
        st.session_state["subtask_list"][task_title].append(subtask_list)
        st.success(f"subtask_list {subtask_list} added under {task_title} !")
    else:
        st.warning("Please enter a subtask_list before adding.")

def add_task(task_title):
    if task_title:
        task = {"title": task_title, "subtasks": [], "completed": False} 
        st.session_state["task_list"].append(task)
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")

def delete_task(task_title):
    st.session_state["task_list"] = [task for task in st.session_state["task_list"] if task["title"] != task_title]
    if task_title in st.session_state["subtask_list"]:
        del st.session_state["subtask_list"][task_title]
    st.success(f"Task '{task_title}' deleted successfully.")


lm , mm , rm = st.columns([1,2,1])

with lm:
    st.write("")

with mm:
    planer_text = st.text_area("I can plan your mission for you :wink:", key = f"planer_text" , placeholder = "like i want learn python , i want you mange my study plan")
    if st.button("plan it :wink:" , key = f"planer_buttom"):
        if planer_text:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "user", "content": planer_text})

            try: #chat make easy
                chatbot_prompt = (
                    f"give it to me easy in task and subtask_list format only (without code and details and description) Headlines only give me at most 1 main task for this topic {planer_text}"
                )
                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text

                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                st.error(f"there error call: {e}")
        else:
            st.warning("Please but your plan before click the button")

with lm:
    st.write("")


LCol , MCol , RCol = st.columns([10,1,10])

with LCol:
    st.title("ChatBot :robot_face:")

    chat_container = st.container(border=True, height=500)
    prompt = st.chat_input("Enter a message")
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        if prompt :
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            try:
                chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
                chatbot_prompt = (
                    f"here is the conversation history:\n{chat_history}\nUser: {prompt}\nAssistant:"
                    "be helpful for user"
                    "ai don't talk a lot"
                )
                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text

            except Exception as e:
                response = f"there a error call: {e}"

            #make stream ai typing 
            with st.chat_message("assistant"): 
                word_by_word_output = st.empty() 
                words = assistant_reply.split()
                displayed_text = ""
                for word in words:
                    displayed_text += word + " "
                    word_by_word_output.markdown(displayed_text)
                    time.sleep(0.1)

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    #button that take the task to right side as task and sub-task
    if st.button("add it to my tasks :arrow_right:"):
        if st.session_state.messages:
            last_message = st.session_state.messages[-1]["content"]

            lines = last_message.split("\n")

            first_line = None  # To store the first line

            for i, line in enumerate(lines):
                line = line.strip() 
                
                if not line:  # skip empty lines
                    continue
                
                if i == 0:  # First non-empty line
                    first_line = line
                    add_task(first_line)  # Add first line as task
                elif i == 2:  # skip the second line as sub-task
                    continue
                else:  # For other lines take it as subtasks
                    add_sub_task(line, first_line)

                
                st.success("the tasks and subtasks added from chatbot response!")
            else:
                st.warning("no response from the chatbot to add as tasks")

with MCol:
    st.title(" ")

with RCol:
    st.title("To-Do List :clipboard:")

    to_do_container = st.container(border=False, height=1500)
    with to_do_container:
        # create big task's
        task_textbox = st.text_input("Enter task: ", key="task_input")
        if st.button("Add task"):
            add_task(st.session_state["task_input"])
            st.rerun()

        st.write("Tasks: ")

        for task in st.session_state["task_list"]:
            with st.expander(f"✅ {task['title']}" if task.get("completed", False) else task["title"]): 
                # button that delete task
                if st.button("Delete Task", key=f"delete_{task['title']}"):
                    delete_task(task["title"])
                    st.rerun()

                # button that take input and create sub-task's
                sub_task_textbox = st.text_input(f"Enter a sub-task for {task['title']}", key=f"input_{task['title']}") 
                if st.button(f"Add Sub-task to {task['title']}", key=f"add_subtask_{task['title']}"):
                    add_sub_task(sub_task_textbox, task["title"])
                    st.rerun()

                total_count = 0
                check_count = 0 

                for sub_task in st.session_state["subtask_list"].get(task["title"], []):
                    total_count += 1
                    checkbox_key = f"checkbox_{task['title']}_{sub_task}"

                    #make to side to but checkbox(sub-task) and delete button(delete sub-task)
                    col1, col2 = st.columns([9, 1]) 
                    with col1:
                        checked = st.checkbox(sub_task, key=checkbox_key)
                    with col2:
                        if st.button("🗑️", key=f"delete_sub_{task['title']}_{sub_task}"):
                            st.session_state["subtask_list"][task["title"]].remove(sub_task)
                            st.rerun()

                    if checked:
                        check_count += 1

                # Progress Bar for Task Completion
                if total_count > 0:
                    progress = check_count / total_count
                    st.progress(progress)  
                    st.write(f"Progress: {int(progress * 100)}%")

                    if progress == 1 and not task.get("completed", False):
                        task["completed"] = True  
                        st.success(f"✅ {task['title']} Completed!")
                        st.rerun()

                # AI helper button
                if st.button("AI HELP :robot_face:", key=f"ai_help_{task['title']}"):
                    chatbot_prompt = f"I have a task called '{task['title']}'"
                    if st.session_state["subtask_list"].get(task["title"]):
                        chatbot_prompt += f" with the following subtasks: {', '.join(st.session_state['subtask_list'][task['title']])}"

                    st.session_state.messages.append({"role": "user", "content": chatbot_prompt})
                    
                    try:
                        chatbot_prompt = f"Help and explain about {chatbot_prompt} and do what the user wants."
                        response = model.generate_content(chatbot_prompt)
                        assistant_reply = response.text
                    except Exception as e:
                        assistant_reply = f"An error occurred: {str(e)}"

                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    st.rerun()