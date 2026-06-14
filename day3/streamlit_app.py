import streamlit as st
import google.generativeai as genai

st.title(":material/airwave: Write Streams")

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Model selection
llm_models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash-lite"]
model_name = st.selectbox("Select a model", llm_models)

# Prompt
example_prompt = "What is Python?"
prompt = st.text_area("Enter prompt", example_prompt)

# Streaming method
streaming_method = st.radio(
    "Streaming Method:",
    ["Direct", "Real Streaming"],
    help="Choose how to stream the response"
)

if st.button("Generate Response"):
    if prompt:
        model = genai.GenerativeModel(model_name)
        
        if streaming_method == "Direct":
            with st.spinner(f"Generating response with `{model_name}`"):
                try:
                    response = model.generate_content(prompt)
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            with st.spinner(f"Streaming response with `{model_name}`"):
                try:
                    response = model.generate_content(
                        prompt,
                        stream=True
                    )
                    result = ""
                    placeholder = st.empty()
                    for chunk in response:
                        if chunk.text:
                            result += chunk.text
                            placeholder.write(result)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a prompt first.")

# Footer
st.divider()
st.caption("Day 3: Write Streams | 30 Days of AI")
