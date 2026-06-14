import streamlit as st
import google.generativeai as genai

st.title(":material/smart_toy: Hello, Cortex!")

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# List available models
st.write("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        st.write(m.name)
