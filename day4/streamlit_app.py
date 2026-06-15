import streamlit as st
import time
import google.generativeai as genai

st.title(":material/cached: Caching your App")

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

@st.cache_data
def call_gemini_llm(prompt_text):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_text)
    return response.text

prompt = st.text_input("Enter your prompt", "Why is the sky blue?")

if st.button("Submit"):
    start_time = time.time()
    response = call_gemini_llm(prompt)
    end_time = time.time()
    
    st.success(f"*Call took {end_time - start_time:.2f} seconds*")
    st.write(response)
    
    st.info("💡 Click Submit again with same prompt — see how fast it is with caching!")

# Footer
st.divider()
st.caption("Day 4: Caching your App | 30 Days of AI")
