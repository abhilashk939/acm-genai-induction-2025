This is a simple web-based chatbot built using Streamlit, LangChain, and the Groq API. It allows users to interact with various powerful language models with very low latency.

I used four different Groq models (llama3-8b-8192, llama3-70b-8192, mixtral-8x7b-32768, gemma-7b-it), and the user can choose which one to chat with from a dropdown menu.

I loaded the Groq API key securely from a .env file to keep it private.

I used LangChain's ConversationChain to manage the chatbot's logic and integrate the language model.

I am holding context across messages by using ConversationBufferMemory from LangChain, which stores the chat history.

The user interface is built with Streamlit, with a sidebar for model selection and a clean chat layout.

I am using Streamlit's session_state to keep the chat history on the screen so the conversation doesn't disappear when the user interacts with the app.

Hope you like it! :-)
