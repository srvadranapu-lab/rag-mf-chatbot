import streamlit as st
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app.rag import generate_answer

st.set_page_config(page_title="MF FAQ Assistant", layout="centered")

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
        answer = generate_answer(query)
        st.markdown("### Answer")
        st.write(answer)