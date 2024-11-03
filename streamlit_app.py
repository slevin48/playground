from streamlit_monaco import st_monaco
import streamlit as st
import openai
import json
import sys
from io import StringIO

# App configs
st.set_page_config(page_title="AI Coding Assistant", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
openai.api_key = st.secrets["OPENAI_API_KEY"]

avatar = {
    "user": "🤓",
    "assistant": "🤖"
}

system_prompt = {"role": "system", "content": "You are a helpful assistant that can help with Python code. Generate code to answer the user's question, in a json object {'code':...}"}
# Initialize session states
if "conversation" not in st.session_state:
    st.session_state.conversation = [system_prompt]
if "code_editor" not in st.session_state:
    st.session_state.code_editor = ""

# Functions
def chatbot(messages,model="gpt-4o-mini"):
    # Generate text with OpenAI
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
    )

    response_message = response.choices[0].message
    return dict(response_message)

def on_chat_input():
    user_input = st.session_state.user_input
    st.session_state.conversation.append({"role": "user", "content": user_input})
    response_message = chatbot(st.session_state.conversation)

    # Parse the JSON response
    try:
        response_content = json.loads(response_message["content"])
        # Update code editor if code is present
        if "code" in response_content and response_content["code"]:
            st.session_state.code_editor = response_content["code"]
            # Add assistant's generated code to conversation
            st.session_state.conversation.append({
                "role": "assistant", 
                "content": "```python\n" + response_content["code"] + "\n```"
            })
    except json.JSONDecodeError as e:
        st.error(f"Error parsing response: {e}")

# Create two columns
col1, col2 = st.columns(2)

# Left column: Chat panel
with col1:
    # st.header("AI Coding Assistant")
    
    # Create a container with a fixed height for the chat
    chat_container = st.container(height=500)
    
    with chat_container:
        if len(st.session_state.conversation) == 1 and st.session_state.conversation[0]["role"] == "system":
            with st.chat_message("assistant", avatar=avatar["assistant"]):
                st.write("Hello! I'm your AI coding assistant. How can I help you with your Python code today?")
        else:
            for message in st.session_state.conversation[1:]:
                with st.chat_message(message["role"], avatar=avatar[message["role"]]):
                    st.write(message["content"])

    # User input
    user_input = st.chat_input(
        "Ask a question about Python or request code help", 
        key="user_input", 
        on_submit=on_chat_input
        )
    
# Right column: Monaco editor
with col2:
    code_input = st_monaco(
        language="python",
        height="478px",
        value=st.session_state.code_editor,
    )
    
    col3, col4 = st.columns(2)
    with col3:
        run_button = st.button("Run")
    if run_button:
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Use code_input instead of st.session_state.code_editor
            exec(code_input)
            output = sys.stdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            sys.stdout = old_stdout
            
        with col4:
            st.code(output, language="python")

# Sidebar controls
with st.sidebar:
    st.title("Settings")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    if st.button("Clear conversation"):
        st.session_state.conversation = [system_prompt]
        st.rerun()
    if st.button("Clear code"):
        st.session_state.code_editor = ""
        st.rerun()
        
    # Example of a prompt
    with st.expander("Example of a prompt", expanded=True):
        st.write("Calculate the 10th element of the Fibonacci sequence.")

    # Debug
    if st.toggle('Debug', value=True):
        st.write(st.session_state)
