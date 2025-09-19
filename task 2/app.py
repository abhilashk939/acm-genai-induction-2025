

!pip install streamlit

!pip install streamlit langchain langchain-groq python-dotenv

import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq

# Initialization

# Load environment variables from a .env file
load_dotenv()
groq_api_key = os.environ.get('GROQ_API_KEY')

def initialize_model(model_name: str, api_key: str) -> ChatGroq:
    """Instantiate a ChatGroq model with the selected name."""
    if not api_key:
        st.error("GROQ_API_KEY not found in your .env file!")
        st.info("Please create a .env file in your project directory and add your Groq API key to it. \n\nExample: GROQ_API_KEY='your_key_here'")
        st.stop()
    try:
        return ChatGroq(groq_api_key=api_key, model_name=model_name)
    except Exception as e:
        st.error(f"Failed to initialize the model: {e}")
        st.stop()
        # Return None or raise an exception if initialization fails
        # Returning None might lead to the ValidationError later
        # Raising an exception is generally better for debugging
        raise e

# --- Streamlit UI Configuration ---

st.set_page_config(
    page_title="Groq Model Chat",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🧠 Groq Model Chat")
st.write("Select a model from the sidebar and start chatting!")

# --- Sidebar for Configuration ---

with st.sidebar:
    st.header("Configuration")
    selected_model = st.selectbox(
        'Choose a Model',
        (
            'llama3-8b-8192',
            'llama3-70b-8192',
            'mixtral-8x7b-32768',
            'gemma-7b-it'
        ),
        key="model_choice"
    )
    st.markdown("---")
    st.markdown(
        "**How to use:**\n"
        "1. Create a `.env` file in this directory.\n"
        "2. Add your key: `GROQ_API_KEY='your-key-here'`\n"
        "3. Select a model.\n"
        "4. Start chatting!"
    )

# --- Chat Logic using LangChain ---

# Initialize session state for chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = selected_model

# If model changes, clear the chat history
if st.session_state.selected_model != selected_model:
    st.session_state.messages = []
    st.session_state.selected_model = selected_model
    st.rerun()

# Display past messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize LangChain components
# Ensure chat_model is initialized correctly
try:
    chat_model = initialize_model(selected_model, groq_api_key)
except Exception as e:
    st.error(f"An error occurred during model initialization: {e}")
    chat_model = None # Assign None if initialization fails

if chat_model is not None:
    memory = ConversationBufferMemory()

    # Restore memory from session state history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            memory.chat_memory.add_user_message(msg["content"])
        elif msg["role"] == "assistant":
            memory.chat_memory.add_ai_message(msg["content"])

    conversation = ConversationChain(llm=chat_model, memory=memory)

    # Input box for user message
    if prompt := st.chat_input("Enter your message..."):
        # Add user message to session state and display
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from the model
        with st.spinner("Generating response..."):
            if chat_model is not None:
                response = conversation.predict(input=prompt)
            else:
                response = "Model not initialized due to a previous error."


        # Add assistant response to session state and display
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# This cell will be removed as its logic is merged into the next cell.
# Handle new user input
# if prompt := st.chat_input("What is on your mind?"):
#     # Display user message and add to session state
#     with st.chat_message("user"):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})

# Handle new user input and get response
if prompt := st.chat_input("What is on your mind?"):
    # Display user message and add to session state
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from the conversation chain
    if 'conversation' in locals() and conversation is not None:
        with st.spinner("Generating response..."):
            response = conversation.predict(input=prompt)

        # Display assistant response and add to session state
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.error("Chat model or conversation chain not initialized.")



