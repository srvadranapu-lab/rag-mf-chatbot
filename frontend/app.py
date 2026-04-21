import streamlit as st
import requests

st.set_page_config(page_title="MF FAQ Assistant", layout="centered", page_icon="📊")

API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0a0f1e;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(56, 100, 255, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 80%, rgba(99, 55, 200, 0.10) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 720px !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    margin-bottom: 2.5rem;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(56, 100, 255, 0.15);
    border: 1px solid rgba(56, 100, 255, 0.35);
    border-radius: 999px;
    color: #7fa3ff;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    margin-bottom: 1.1rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 5vw, 2.9rem);
    color: #f0f4ff;
    line-height: 1.15;
    margin: 0 0 0.6rem;
    letter-spacing: -0.01em;
}
.hero-title em {
    font-style: italic;
    color: #7fa3ff;
}
.hero-sub {
    font-size: 0.9rem;
    color: #6b7a99;
    font-weight: 400;
    letter-spacing: 0.01em;
    margin: 0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,100,255,0.3), transparent);
    margin: 0.5rem 0 2rem;
}

/* ── Section label ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4a5572;
    margin-bottom: 0.75rem;
}

/* ── Suggestion chips ── */
.stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #b0bdd8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 400 !important;
    padding: 0.6rem 1rem !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    margin-bottom: 0.5rem !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    background: rgba(56, 100, 255, 0.12) !important;
    border-color: rgba(56, 100, 255, 0.4) !important;
    color: #d0daff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(56, 100, 255, 0.15) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8edf8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(56, 100, 255, 0.6) !important;
    box-shadow: 0 0 0 3px rgba(56, 100, 255, 0.12) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a4460 !important;
}
.stTextInput label {
    color: #6b7a99 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-color: #3864ff transparent transparent transparent !important;
}

/* ── Answer card ── */
.answer-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(56, 100, 255, 0.2);
    border-left: 3px solid #3864ff;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
    position: relative;
    animation: fadeSlideUp 0.35s ease both;
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.answer-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #3864ff;
    margin-bottom: 0.7rem;
}
.answer-text {
    color: #c8d4f0;
    font-size: 0.95rem;
    line-height: 1.7;
    font-weight: 300;
}

/* ── Error card ── */
.error-card {
    background: rgba(220, 50, 80, 0.07);
    border: 1px solid rgba(220, 50, 80, 0.25);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    margin-top: 1.2rem;
    color: #f08090;
    font-size: 0.88rem;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    color: #2e3a54;
    font-size: 0.75rem;
    letter-spacing: 0.03em;
}
.footer span { color: #3a4a6b; }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Powered · Facts Only</div>
    <h1 class="hero-title">Mutual Fund<br><em>FAQ Assistant</em></h1>
    <p class="hero-sub">Ask anything about mutual funds — expense ratios, lock-ins, statements, exit loads.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Suggestion chips ──────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Quick questions</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("📉  Expense ratio of HDFC Top 100"):
        st.session_state.query = "What is expense ratio of HDFC Top 100 Fund?"
    if st.button("🔒  ELSS lock-in period"):
        st.session_state.query = "What is ELSS lock-in period?"

with col2:
    if st.button("📄  How to download MF statement"):
        st.session_state.query = "How to download mutual fund statement?"
    if st.button("🚪  Exit load — Balanced Advantage Fund"):
        st.session_state.query = "What is exit load of HDFC Balanced Advantage Fund?"

st.markdown("<br>", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
query = st.text_input(
    "Your question",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What is the NAV of Parag Parikh Flexi Cap Fund?",
)

# ── Answer ────────────────────────────────────────────────────────────────────
if query:
    with st.spinner("Thinking…"):
        try:
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()
            answer = response.json()["answer"]
            st.markdown(f"""
            <div class="answer-card">
                <div class="answer-label">Answer</div>
                <div class="answer-text">{answer}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="error-card">
                ⚠️ Could not fetch an answer — <strong>{str(e)}</strong>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Data sourced from <span>HDFC AMC · AMFI · SEBI · Groww</span><br>
    No investment advice. For informational purposes only.
</div>
""", unsafe_allow_html=True)