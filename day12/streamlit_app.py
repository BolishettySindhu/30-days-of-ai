import streamlit as st
from groq import Groq
import time

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def call_llm(prompt_text: str) -> str:
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt_text}]
    )
    return response.choices[0].message.content

st.title(":material/chat: Chatbot with Streaming")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

with st.sidebar:
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

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = "\n\n".join([
        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
        for msg in st.session_state.messages
    ])
    full_prompt = f"{conversation}\n\nAssistant:"

    def stream_generator():
        try:
            response_text = call_llm(full_prompt)
            for word in response_text.split(" "):
                yield word + " "
                time.sleep(0.02)
        except Exception as e:
            yield f"Error: {str(e)}"

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = st.write_stream(stream_generator)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.divider()
st.caption("Day 12: Streaming Responses | 30 Days of AI")
