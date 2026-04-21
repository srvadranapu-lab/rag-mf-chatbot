import streamlit as st
import requests

st.set_page_config(page_title="MF FAQ Assistant", layout="centered")

# 🔴 REPLACE WITH YOUR ACTUAL RENDER URL
API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# Title
st.title("Mutual Fund FAQ Assistant")

# Disclaimer
st.markdown("**Facts-only. No investment advice.**")

# Example Questions
st.markdown("**Try asking:**")
st.markdown("- What is expense ratio of HDFC Top 100 Fund?")
st.markdown("- What is ELSS lock-in period?")
st.markdown("- How to download mutual fund statement?")

# Input
query = st.text_input("Ask your question:")

if query:
    with st.spinner("Fetching answer..."):
        try:
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()
            answer = response.json()["answer"]
        except Exception as e:
            answer = f"Error: {str(e)}"

        st.markdown("### Answer")
        st.write(answer)

# Footer
st.markdown("---")
st.caption("Data sourced from HDFC AMC, AMFI, SEBI, and Groww.")