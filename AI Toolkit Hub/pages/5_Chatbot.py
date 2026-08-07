import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(
    page_title="ChatGPT Assistant",
    page_icon="💬",
    layout="wide"
)

# Check authentication
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please log in first!")
    st.stop()

# Initialize OpenAI client
api_key = st.secrets.get("OPENAI_API_KEY")
base_url = st.secrets.get("OPENAI_BASE_URL", "https://api.bluesminds.com/v1")
client = OpenAI(api_key=api_key, base_url=base_url, timeout=30.0)

# Title
st.title("💬 ChatGPT - OpenAI API")
st.caption("Powered by AI Models")

# Domain-specific system prompts
DOMAIN_PROMPTS = {
    "Cybersecurity": """You are a cybersecurity expert assistant.
Analyze incidents, threats, and provide technical guidance.""",
    
    "Data Science": """You are a data science expert assistant.
Help with analysis, visualization, and statistical insights.""",
    
    "IT Operations": """You are an IT operations expert assistant.
Help troubleshoot issues, optimize systems, and manage tickets."""
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'selected_domain' not in st.session_state:
    st.session_state.selected_domain = "Cybersecurity"

# Sidebar with controls
with st.sidebar:
    st.subheader("User Info")
    st.write(f"👤 {st.session_state.username}")
    st.write(f"🔑 {st.session_state.role.upper()}")
    
    st.markdown("---")
    st.subheader("Domain Selection")
    
    # Domain selector
    domain = st.selectbox(
        "Choose Domain",
        ["Cybersecurity", "Data Science", "IT Operations"],
        index=["Cybersecurity", "Data Science", "IT Operations"].index(st.session_state.selected_domain)
    )
    
    # Update domain if changed
    if domain != st.session_state.selected_domain:
        st.session_state.selected_domain = domain
        st.session_state.messages = []  # Clear chat when domain changes
        st.success(f"Switched to {domain} domain")
        st.rerun()
    
    # Display current system prompt
    with st.expander("View System Prompt"):
        st.code(DOMAIN_PROMPTS[domain], language="text")
    
    st.markdown("---")
    st.subheader("Chat Controls")
    
    # Display message count
    message_count = len([m for m in st.session_state.messages if m["role"] != "system"])
    st.metric("Messages", message_count)
    
    # Clear chat button
    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    # Model selection
    try:
        models_data = client.models.list()
        available_models = [m.id for m in models_data.data] if models_data and hasattr(models_data, 'data') and len(models_data.data) > 0 else ["gpt-5.5", "gpt-4o-mini"]
    except Exception:
        available_models = ["gpt-5.5", "gpt-4o-mini", "gpt-4o"]

    model = st.selectbox(
        "Model",
        available_models,
        index=0
    )

# Display all previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Say something...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to session state
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Prepare messages with system prompt
    messages_with_system = [
        {"role": "system", "content": DOMAIN_PROMPTS[st.session_state.selected_domain]}
    ] + st.session_state.messages
    
    # Call OpenAI API with fallback and error handling
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages_with_system,
                    stream=False
                )
                full_reply = completion.choices[0].message.content or "No response content returned."
                st.markdown(full_reply)
                
                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_reply
                })
            except Exception as e:
                error_msg = str(e)
                st.error(f"⚠️ API Response Error: {error_msg}")
                if "504" in error_msg or "timeout" in error_msg.lower():
                    st.info("💡 The API Proxy gateway timed out. Please click send again in a moment.")
                elif "403" in error_msg or "access" in error_msg.lower():
                    st.info(f"💡 The model '{model}' is not accessible on your API key. Try switching model in the sidebar.")
