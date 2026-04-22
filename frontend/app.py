import streamlit as st
import requests

st.set_page_config(page_title="MF FAQ Assistant", layout="centered")

API_URL = "https://rag-mf-chatbot-1259.onrender.com/ask"

# Title
st.title("📊 Mutual Fund FAQ Assistant")

# Subtitle / Disclaimer
st.markdown("**Facts-only. No investment advice.**")

st.markdown("---")

# Example buttons
st.markdown("### 🔍 Try a question:")

col1, col2 = st.columns(2)

with col1:
    if st.button("Expense ratio of HDFC Top 100 Fund"):
        st.session_state.query = "What is expense ratio of HDFC Top 100 Fund?"

    if st.button("ELSS lock-in period"):
        st.session_state.query = "What is ELSS lock-in period?"

with col2:
    if st.button("Download MF statement"):
        st.session_state.query = "How to download mutual fund statement?"

    if st.button("Exit load of Balanced Advantage Fund"):
        st.session_state.query = "What is exit load of HDFC Balanced Advantage Fund?"

# Input box
query = st.text_input("Ask your question:", value=st.session_state.get("query", ""))

# Chat response
if query:
    with st.spinner("Fetching answer..."):
        try:
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()
            answer = response.json()["answer"]
        except Exception as e:
            answer = f"Error: {str(e)}"

        st.markdown("### 💬 Answer")
        st.success(answer)

# Footer
st.markdown("---")
st.caption("Data sourced from HDFC AMC, AMFI, SEBI, and Groww.")