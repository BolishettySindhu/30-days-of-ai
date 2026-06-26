import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")


def call_llm(prompt_text):
    response = model.generate_content(prompt_text)
    return response.text


st.title("💬 Customizable Chatbot")

# Initialize system prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful pirate assistant named Captain Starlight. "
        "You speak with pirate slang, use nautical metaphors, "
        "and end sentences with 'Arrr!' when appropriate."
    )

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ahoy! Captain Starlight here, ready to help ye navigate the high seas of knowledge! Arrr!"
        }
    ]

# Sidebar
with st.sidebar:

    st.header("🎭 Bot Personality")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🏴‍☠ Pirate"):
            st.session_state.system_prompt = (
                "You are a helpful pirate assistant named Captain Starlight. "
                "You speak with pirate slang."
            )
            st.rerun()

    with col2:
        if st.button("👨‍🏫 Teacher"):
            st.session_state.system_prompt = (
                "You are Professor Ada, a patient teacher. Explain everything clearly."
            )
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        if st.button("😂 Comedian"):
            st.session_state.system_prompt = (
                "You are a funny comedian who always includes humor."
            )
            st.rerun()

    with col4:
        if st.button("🤖 Robot"):
            st.session_state.system_prompt = (
                "You are UNIT-7, a logical robot assistant."
            )
            st.rerun()

    st.divider()

    st.text_area(
        "System Prompt",
        key="system_prompt",
        height=180
    )

    st.divider()

    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    ai_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])

    st.metric("Your Messages", user_msgs)
    st.metric("AI Responses", ai_msgs)

    if st.button("Clear History"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm ready to help."
            }
        ]
        st.rerun()

# Display messages

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat

if prompt := st.chat_input("Type your message..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        def stream_generator():

            conversation = "\n\n".join([
                f"{msg['role'].capitalize()}: {msg['content']}"
                for msg in st.session_state.messages
            ])

            full_prompt = f"""
System Prompt:
{st.session_state.system_prompt}

Conversation:
{conversation}

Respond to the user's latest message.
"""

            response = call_llm(full_prompt)

            for word in response.split():
                yield word + " "
                time.sleep(0.02)

        with st.spinner("Thinking..."):
            response = st.write_stream(stream_generator)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    st.rerun()

st.divider()
st.caption("Day 13: Adding a System Prompt | 30 Days of AI")
