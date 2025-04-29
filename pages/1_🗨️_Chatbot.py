from openai import OpenAI
import streamlit as st
import time
from src.chatbot.flow import ChatbotFlow

st.set_page_config(
    page_title="Thailand Trip Companion",
    page_icon="🌴",
    layout="centered"
)

st.title("🇹🇭 Ask About Thailand 🐘")

if "messages" not in st.session_state:
    st.session_state.messages = []    # Chat history

if "flow" not in st.session_state:
    st.session_state.flow = None      # Store the Flow object

# Render existing conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Thailand ..."):
    # 1. Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Build or reuse the Crew
    if not st.session_state.flow:
        st.session_state.flow = ChatbotFlow()

    # 3. Get the response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Get the complete response first
        with st.spinner("Thinking..."):
            inputs = {"query": prompt}
            result = st.session_state.flow.kickoff(inputs=inputs)
        
        # Split by lines first to preserve code blocks and other markdown
        lines = result.split('\n')
        for i, line in enumerate(lines):
            full_response += line
            if i < len(lines) - 1:  # Don't add newline to the last line
                full_response += '\n'
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.15)  # Adjust the speed as needed
        
        # Show the final response without the cursor
        message_placeholder.markdown(full_response)

    # 4. Save assistant's message to session
    st.session_state.messages.append({"role": "assistant", "content": result})
