import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def call_llm(prompt_text: str) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_text)
    return response.text

st.title(":material/account_circle: Adding Avatars and Error Handling")

# Initialize system prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Sidebar
with st.sidebar:
    st.header(":material/settings: Settings")
    
    st.subheader(":material/palette: Avatars")
    user_avatar = st.selectbox(
        "Your Avatar:",
        ["👤", "🧑‍💻", "👨‍🎓", "👩‍🔬", "🦸", "🧙"],
        index=0
    )
    assistant_avatar = st.selectbox(
        "Assistant Avatar:",
        ["🤖", "🧠", "✨", "🎯", "💡", "🌟"],
        index=0
    )
    
    st.divider()
    
    st.subheader(":material/description: System Prompt")
    st.text_area(
        "Customize behavior:",
        height=100,
        key="system_prompt",
        help="Define how the AI should behave and respond"
    )
    
    st.divider()
    
    st.subheader(":material/bug_report: Debug Mode")
    simulate_error = st.checkbox(
        "Simulate API Error",
        value=False,
        help="Enable this to test the error handling mechanism"
    )
    
    st.divider()
    
    st.header("Conversation Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    st.metric("Your Messages", user_msgs)
    st.metric("AI Responses", assistant_msgs)
    
    if st.button("Clear History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
        st.rerun()

# Display messages
for message in st.session_state.messages:
    avatar = user_avatar if message["role"] == "user" else assistant_avatar
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar=assistant_avatar):
        try:
            if simulate_error:
                raise Exception("Simulated API error: Service temporarily unavailable (429)")
            
            def stream_generator():
                conversation = "\n\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                full_prompt = f"""{st.session_state.system_prompt}

Here is the conversation so far:
{conversation}

Respond to the user's latest message."""
                
                try:
                    response_text = call_llm(full_prompt)
                    for word in response_text.split(" "):
                        yield word + " "
                        time.sleep(0.02)
                except Exception as e:
                    yield f"Error: {str(e)}"
            
            with st.spinner("Processing"):
                response = st.write_stream(stream_generator)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
            
        except Exception as e:
            error_message = f"I encountered an error: {str(e)}"
            st.error(error_message)
            st.info(":material/lightbulb: **Tip:** This might be a temporary issue. Try again in a moment!")

st.divider()
st.caption("Day 14: Adding Avatars and Error Handling | 30 Days of AI")
