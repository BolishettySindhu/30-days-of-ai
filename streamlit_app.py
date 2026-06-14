import streamlit as st
import anthropic

st.title(":material/smart_toy: Hello, Cortex!")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

model = "claude-sonnet-4-5"
prompt = st.text_input("Enter your prompt:")

if st.button("Generate Response"):
    if prompt:
        with st.spinner("Generating response..."):
            message = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            response = message.content[0].text
            st.write(response)
    else:
        st.warning("Please enter a prompt first.")

st.divider()
st.caption("Day 2: Hello, Cortex! | 30 Days of AI")
