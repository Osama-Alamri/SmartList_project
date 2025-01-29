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

if "suptask_list" not in st.session_state:
    st.session_state["suptask_list"] = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

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
        task = {"title": task_title, "subtasks": []} 
        st.session_state["task_list"].append(task)
        st.success("Task added!")
    else:
        st.warning("Please enter a task before adding.")

def delete_task(task_title):
    st.session_state["task_list"] = [task for task in st.session_state["task_list"] if task["title"] != task_title]
    if task_title in st.session_state["suptask_list"]:
        del st.session_state["suptask_list"][task_title]
    st.success(f"Task '{task_title}' deleted successfully.")


lm , mm , rm = st.columns([1,2,1])

with lm:
    st.write("")

with mm:
    planer_text = st.text_area("I can plan your mission for you :wink:", key = f"planer_text" , placeholder = "like i want learn python , i want you mange my study plan")
    if st.button("plan it :wink:" , key = f"planer_buttom"):
        if planer_text:
            st.session_state.messages = [] # Clear previous chat history````
            st.session_state.messages.append({"role": "user", "content": planer_text})

            try: #chat prompt for text area (easy details)
                chatbot_prompt = (
                    f"give it to me easy in task and sup-task format only (without code and details and description) Headlines only give me at most 1 main task for this topic {planer_text}"
                )
                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text

                st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

            except Exception as e:
                st.error(f"Error generating mission plan: {e}")
        else:
            st.warning("Please provide a mission description.")

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
                task_data = "\n".join([
                    f"{idx + 1}. {task['title']}" 
                    for idx, task in enumerate(st.session_state["task_list"])
                ])
                chatbot_prompt = (
                    f"help the user about {prompt} don't talk a lot "
                )

                response = model.generate_content(chatbot_prompt)
                assistant_reply = response.text

            except Exception as e:
                response = f"An error occurred: {str(e)}"


            with st.chat_message("assistant"):
                word_by_word_output = st.empty() # Placeholder for dynamic word updates
                words = assistant_reply.split()
                displayed_text = ""
                for word in words:
                    displayed_text += word + " "
                    word_by_word_output.markdown(displayed_text)
                    time.sleep(0.1)

            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    if st.button("add it to my tasks :arrow_right:"):
            # Check the latest assistant message to extract tasks and subtasks
        if st.session_state.messages:
            last_message = st.session_state.messages[-1]["content"]

            lines = last_message.split("\n")

            first_line = None  # To store the first line

            for i, line in enumerate(lines):
                line = line.strip()  # Clean up any leading/trailing spaces
                
                if not line:  # Skip empty lines
                    continue
                
                if i == 0:  # First non-empty line
                    first_line = line
                    add_task(first_line)  # Add first line as task
                elif i == 2:  # Skip the second line
                    continue
                else:  # For other lines, treat them as subtasks
                    add_sup_task(line, first_line)

                
                st.success("Tasks and subtasks added from chatbot response!")
            else:
                st.warning("No response from the chatbot to add as tasks.")
with MCol:
    st.title(" ")


with RCol:
    st.title("To-Do List :clipboard:")

    to_do_container = st.container(border=False, height=1500)
    with to_do_container:
        task_textbox = st.text_input("Enter task: ", key="task_input")
        if st.button("Add task"):
            add_task(st.session_state["task_input"])

        st.write("Tasks: ")
    
        for task in st.session_state["task_list"]: 
            with st.expander(task["title"]): 
                if st.button("delete this task", key=f"delete_{task['title']}"):
                    delete_task(task["title"])
                    st.session_state.rerun_trigger += 1  

        
                sup_task_textbox = st.text_input(f"Enter a sub-task for {task['title']}") 
                if st.button(f"Add Sup-task to {task['title']}", key=f"add_suptask_{task['title']}"):
                    add_sup_task(sup_task_textbox, task["title"]) 
                total_count = 0
                check_count = 0 
    
                for sup_task in st.session_state["suptask_list"].get(task["title"], []):
                    total_count += 1
                    if st.checkbox(sup_task, key=f"checkbox_{task['title']}_{sup_task}"):
                        check_count += 1

                if total_count > 0:
                    progress = check_count / total_count
                    st.progress(progress)  # Display progress bar
                    
                    progress_text = f"Progress: {int(progress * 100)}%"
                    task_completed = False
                    if progress == 1:
                        progress_text = f"✅ {task['title']} Completed!"
                        task_completed = True  # Mark as completed
                        

                    st.write(progress_text) 
                    



                if st.button("AI HELP :robot_face:", key=f"ai_help_{task['title']}"):
                    chatbot_prompt = f"I have a task called '{task['title']}'."
                    if st.session_state["suptask_list"].get(task["title"]):
                        chatbot_prompt += f" It has the following subtasks: {', '.join(st.session_state['suptask_list'][task['title']])}"
                    st.session_state.messages.append({"role": "user", "content": chatbot_prompt})

                    try:
                        chatbot_prompt = (
                        f"help and explain about {chatbot_prompt} and do what user want"
                             )
                        response = model.generate_content(chatbot_prompt)
                        assistant_reply = response.text

                    except Exception as e:
                        response = f"An error occurred: {str(e)}"

            # send to chatbot area
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    st.rerun()