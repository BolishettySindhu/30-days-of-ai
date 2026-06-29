import streamlit as st
import time
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Session state initialization
if "latest_results" not in st.session_state:
    st.session_state.latest_results = None

def run_model(model_name: str, prompt: str) -> dict:
    """Execute model and collect metrics."""
    start = time.time()
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        text = response.text
    except Exception as e:
        text = f"Error: {str(e)}"
    
    latency = time.time() - start
    tokens = int(len(text.split()) * 4/3)
    
    return {
        "latency": latency,
        "tokens": tokens,
        "response_text": text
    }

def display_metrics(results: dict, model_key: str):
    latency_col, tokens_col = st.columns(2)
    latency_col.metric("Latency (s)", f"{results[model_key]['latency']:.1f}")
    tokens_col.metric("Tokens", results[model_key]['tokens'])

def display_response(container, results: dict, model_key: str):
    with container:
        with st.chat_message("user"):
            st.write(results["prompt"])
        with st.chat_message("assistant"):
            st.write(results[model_key]["response_text"])

# Model selection
llm_models = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
]

st.title(":material/compare: Select Models")
col_a, col_b = st.columns(2)

col_a.write("**Model A**")
model_a = col_a.selectbox("Model A", llm_models, key="model_a", label_visibility="collapsed")

col_b.write("**Model B**")
model_b = col_b.selectbox("Model B", llm_models, key="model_b", index=1, label_visibility="collapsed")

# Response containers
st.divider()
col_a, col_b = st.columns(2)
results = st.session_state.latest_results

for col, model_name, model_key in [(col_a, model_a, "model_a"), (col_b, model_b, "model_b")]:
    with col:
        st.subheader(model_name)
        container = st.container(height=400, border=True)
        
        if results:
            display_response(container, results, model_key)
        
        st.caption("Performance Metrics")
        if results:
            display_metrics(results, model_key)
        else:
            latency_col, tokens_col = st.columns(2)
            latency_col.metric("Latency (s)", "—")
            tokens_col.metric("Tokens", "—")

# Chat input
st.divider()
if prompt := st.chat_input("Enter your message to compare models"):
    with st.status(f"Running {model_a}..."):
        result_a = run_model(model_a, prompt)
    with st.status(f"Running {model_b}..."):
        result_b = run_model(model_b, prompt)
    
    st.session_state.latest_results = {
        "prompt": prompt,
        "model_a": result_a,
        "model_b": result_b
    }
    st.rerun()

st.divider()
st.caption("Day 15: Model Comparison Arena | 30 Days of AI")
