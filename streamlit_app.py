from streamlit_monaco import st_monaco
import streamlit as st

st.set_page_config(page_title="AI Coding Assistant", page_icon="🤖", layout="wide")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Create two columns
col1, col2 = st.columns(2)

# Left column: Chat panel
with col1:
    # st.header("AI Coding Assistant")
    
    # Create a container with a fixed height for the chat
    chat_container = st.container(height=500)
    
    with chat_container:
        if not st.session_state.conversation:
            with st.chat_message("assistant", avatar="🤖"):
                st.write("Hello! I'm your AI coding assistant. How can I help you with your Python code today?")
        else:
            for role, message in st.session_state.conversation:
                with st.chat_message(role, avatar="🤖" if role == "assistant" else "👤"):
                    st.write(message)

    # User input
    user_input = st.chat_input("Ask a question about Python or request code help", key="user_input")
    if user_input:
        st.session_state.conversation.append(("user", user_input))
        # Here you would typically call your AI model to get a response
        # For now, we'll use a placeholder response
        ai_response = "This is a placeholder response. In a real application, you would integrate with an AI model here."
        st.session_state.conversation.append(("assistant", ai_response))
        st.rerun()

# Right column: Monaco editor
with col2:
    # st.header("Python Editor")
    example_code = "# This is Python code\n# in the Monaco editor\nprint('Hello, Monaco!')"
    code = st_monaco(language="python",height="478px",value=example_code)

    if st.button("Run"):
        try:
            # Execute the code
            exec(code)
        except Exception as e:
            st.error(f"Error: {e}")




