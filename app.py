import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Initialize or load chat sessions
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = []
    st.session_state.current_chat_index = -1  # No chat is selected initially

# Function to start a new chat session
def start_new_chat():
    new_chat = {
        "id": len(st.session_state.chat_sessions) + 1,
        "title": None,  # The title will be generated based on the first user message
        "history": [],
        "session": model.start_chat(history=[])
    }
    st.session_state.chat_sessions.append(new_chat)
    st.session_state.current_chat_index = len(st.session_state.chat_sessions) - 1

# Sidebar for history and chat management
with st.sidebar:
    st.title("Chat History")

    # New Chat Button
    if st.button("➕ New Chat"):
        start_new_chat()

    # Search input for filtering chat history
    search_query = st.text_input("Search History")

    # Display chat titles and allow selection
    for i, chat in enumerate(st.session_state.chat_sessions):
        button_label = chat['title'] if chat['title'] else f"Chat {chat['id']}"
        if search_query.lower() in button_label.lower():
            if st.button(button_label):
                st.session_state.current_chat_index = i

# Main chat interface
st.title("🤖 Chat-Bot")

if st.session_state.current_chat_index != -1:
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_index]

    # Display the chat history in the main area
    for message in current_chat["history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    # Input field for user's message
    user_prompt = st.chat_input("Ask Gemini-Pro...")

    if user_prompt:
        # Set the chat title based on the first user message if it's not set
        if current_chat["title"] is None:
            current_chat["title"] = user_prompt

        # Add user's message to chat history and display it
        current_chat["history"].append({
            "role": "user",
            "text": user_prompt,
            "date": datetime.now()
        })
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = current_chat["session"].send_message(user_prompt)

        # Add Gemini-Pro's response to chat history and display it
        current_chat["history"].append({
            "role": "assistant",
            "text": gemini_response.text,
            "date": datetime.now()
        })
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
else:
    st.write("Start a new chat to begin!")
