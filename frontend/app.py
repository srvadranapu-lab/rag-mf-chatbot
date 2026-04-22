import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MF FAQ Assistant", layout="wide")

API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ---------------- THEME STATE ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle function
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ---------------- COLORS ----------------
bg_color = "#0E1117" if st.session_state.dark_mode else "#F3FFF8"
text_color = "#FFFFFF" if st.session_state.dark_mode else "#000000"
card_bg = "#1C1F26" if st.session_state.dark_mode else "#FFFFFF"
border_color = "#2E3138" if st.session_state.dark_mode else "#E5E7EB"

# ---------------- GLOBAL CSS ----------------
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}

.main {{
    background-color: {bg_color};
}}

.card {{
    background: {card_bg};
    border: 1px solid {border_color};
    padding: 16px;
    border-radius: 12px;
    text-align: center;
}}

.stat-box {{
    border: 1px solid {border_color};
    border-radius: 10px;
    padding: 14px;
    text-align: center;
    font-weight: 600;
    background: {card_bg};
}}

.header-pill {{
    border: 1px solid {border_color};
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
}}

hr {{
    border: none;
    border-top: 1px solid {border_color};
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([6, 3, 1])

with col1:
    st.markdown("<h2 style='color:#00D09C; font-weight:bold;'>Groww</h2>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='header-pill'>HDFC AMC · Facts Only</div>", unsafe_allow_html=True)

with col3:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        toggle_theme()

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- HERO SECTION ----------------
st.markdown(
    "<h1 style='text-align:center; font-size:56px; font-weight:800;'>STOP GUESSING</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:20px;'>Get fund facts you can actually trust</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:14px;'>"
    "Expense ratios, exit loads, SIP minimums, ELSS lock-ins — sourced directly from HDFC AMC, SEBI, and AMFI documents. "
    "Every answer includes a citation link."
    "</p>",
    unsafe_allow_html=True
)

# ---------------- SAMPLE QUESTIONS ----------------
st.markdown("###", unsafe_allow_html=True)

q1, q2, q3, q4 = st.columns(4)

if "query" not in st.session_state:
    st.session_state.query = ""

with q1:
    if st.button("Expense Ratio"):
        st.session_state.query = "What is expense ratio of HDFC Top 100 Fund?"

with q2:
    if st.button("ELSS Lock-in"):
        st.session_state.query = "What is ELSS lock-in period?"

with q3:
    if st.button("SIP Minimum"):
        st.session_state.query = "What is minimum SIP for HDFC Flexi Cap Fund?"

with q4:
    if st.button("Exit Load"):
        st.session_state.query = "What is exit load of HDFC Balanced Advantage Fund?"

# ---------------- STATS ROW ----------------
s1, s2, s3, s4 = st.columns(4)

s1.markdown("<div class='stat-box'>15+ Official Sources</div>", unsafe_allow_html=True)
s2.markdown("<div class='stat-box'>100% Cited Answers</div>", unsafe_allow_html=True)
s3.markdown("<div class='stat-box'>₹500 Min SIP (HDFC)</div>", unsafe_allow_html=True)
s4.markdown("<div class='stat-box'>3 yrs ELSS Lock-in</div>", unsafe_allow_html=True)

st.markdown("###", unsafe_allow_html=True)

# ---------------- FEATURE CARDS ----------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='card'>📊 <b>Expense Ratios</b><br><small>Exact ratios from official HDFC AMC fact sheets — no guesswork.</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>📉 <b>SIP Minimums</b><br><small>Minimum SIP and lumpsum thresholds straight from fund documents.</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>📄 <b>Statements</b><br><small>Step-by-step guides for CAS and capital gains downloads.</small></div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>🔒 <b>ELSS Lock-ins</b><br><small>Lock-in periods and tax-saving eligibility with SEBI citations.</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>💸 <b>Exit Loads</b><br><small>Redemption charges and applicable timeframes, source-backed.</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>🚫 <b>Zero Hallucinations</b><br><small>If data is unavailable, explicitly say so. No fabricated answers.</small></div>", unsafe_allow_html=True)

# ---------------- QUERY INPUT ----------------
st.markdown("<hr>", unsafe_allow_html=True)

query = st.text_input("Ask your question:", value=st.session_state.query)

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

# ---------------- FOOTER ----------------
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center; font-size:12px;'>"
    "HDFC AMC VERIFIED · SEBI REGISTERED · AMFI DATA · NO PII STORED · FACTS ONLY"
    "</p>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; font-size:10px;'>"
    "Data from HDFC AMC · AMFI · SEBI · Groww · Facts only · No investment advice · No PII stored"
    "</p>",
    unsafe_allow_html=True
)