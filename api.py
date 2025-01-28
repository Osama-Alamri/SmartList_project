import requests
import streamlit as st

# Streamlit app title
st.title("Gemini ChatBot")

# Gemini API details
API_KEY = "your_actual_gemini_api_key"  # Replace with your actual Gemini API key
BASE_URL = "https://api.gemini.com/v1/conversations"  # Replace with the correct endpoint if needed

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to the chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to Gemini API
    with st.chat_message("assistant"):
        try:
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "gemini-1.5",  # Update with the correct model name if needed
                "messages": st.session_state["messages"],  # Send chat history
            }
            response = requests.post(BASE_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes

            # Extract assistant response
            response_data = response.json()
            assistant_response = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")
            st.markdown(assistant_response)
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            assistant_response = "Sorry, I couldn't process your request."

    # Add assistant's response to the chat history
    st.session_state["messages"].append({"role": "assistant", "content": assistant_response})
