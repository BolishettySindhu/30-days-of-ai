import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Cached LLM Function
@st.cache_data
def call_gemini_llm(prompt_text):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt_text)
    return response.text

# --- App UI ---
st.title(":material/post: LinkedIn Post Generator")

# Input widgets
content = st.text_input("Content URL or Topic:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):
    prompt = f"""
    You are an expert social media manager. Generate a LinkedIn post based on the following:
    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL or topic: {content}
    Generate only the LinkedIn post text. Use dash for bullet points.
    """
    
    with st.spinner("Generating post..."):
        try:
            response = call_gemini_llm(prompt)
            st.subheader("Generated Post:")
            st.markdown(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Day 5: Build a Post Generator App | 30 Days of AI")
