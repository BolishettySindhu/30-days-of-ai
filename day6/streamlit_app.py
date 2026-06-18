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
st.title(":material/post: LinkedIn Post Generator v2")

# Input widgets
content = st.text_input("Content URL or Topic:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):

    # Initialize the status container
    with st.status("Starting engine...", expanded=True) as status:

        # Step 1: Construct Prompt
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
        prompt = f"""
        You are an expert social media manager. Generate a LinkedIn post based on the following:
        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this URL or topic: {content}
        Generate only the LinkedIn post text. Use dash for bullet points.
        """

        # Step 2: Call API
        st.write(":material/flash_on: Generating: contacting Gemini AI...")

        try:
            response = call_gemini_llm(prompt)

            # Step 3: Update Status to Complete
            st.write(":material/check_circle: Post generation completed!")
            status.update(label="Post Generated Successfully!", state="complete", expanded=False)

            # Display Result
            st.subheader("Generated Post:")
            st.markdown(response)

        except Exception as e:
            status.update(label="Error occurred!", state="error", expanded=False)
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("Day 6: Status UI for Long-Running Task | 30 Days of AI")
