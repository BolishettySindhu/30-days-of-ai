import streamlit as st
import google.generativeai as genai

st.title(":material/smart_toy: Hello, Cortex!")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = st.text_input("Enter your prompt:")

if st.button("Generate Response"):
    if prompt:
        with st.spinner("Generating response..."):
            response = model.generate_content(prompt)
            st.write(response.text)
    else:
        st.warning("Please enter a prompt first.")

st.divider()
st.caption("Day 2: Hello, Cortex! | 30 Days of AI")
