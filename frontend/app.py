import streamlit as st
import requests

st.set_page_config(
    page_title="FundFacts – MF FAQ Assistant",
    layout="centered",
    page_icon="💹",
    initial_sidebar_state="collapsed",
)

API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ─── Session state defaults ──────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

# ─── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] { font-family: 'Bricolage Grotesque', sans-serif; }

.stApp {
    background: #f7f5f2;
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important;
    padding-bottom: 4rem !important;
    max-width: 780px !important;
}

/* ── Navbar ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 0 1rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #e8e4de;
}
.navbar-brand {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: -0.02em;
}
.navbar-brand .dot { color: #2563eb; }
.navbar-pill {
    background: #eef2ff;
    color: #2563eb;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.28rem 0.8rem;
    border-radius: 999px;
    border: 1px solid #c7d7fd;
}

/* ── Hero ── */
.hero {
    padding: 3rem 0 2rem;
    text-align: center;
}
.hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748b;
    padding: 0.3rem 0.9rem;
    margin-bottom: 1.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.hero-tag .green-dot {
    width: 6px; height: 6px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
}
.hero-title {
    font-family: 'Lora', serif;
    font-size: clamp(1.9rem, 5vw, 2.9rem);
    font-weight: 600;
    color: #0f172a;
    line-height: 1.2;
    letter-spacing: -0.02em;
    margin: 0 0 1rem;
}
.hero-title .accent { font-style: italic; color: #2563eb; }
.hero-desc {
    color: #64748b;
    font-size: 0.97rem;
    font-weight: 400;
    line-height: 1.7;
    max-width: 520px;
    margin: 0 auto 2rem;
}

/* ── Stats row ── */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.5rem;
}
.stat-card {
    background: #fff;
    border: 1px solid #e8e4de;
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stat-val { font-size: 1.3rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em; margin-bottom: 0.2rem; }
.stat-val.blue { color: #2563eb; }
.stat-lbl { font-size: 0.68rem; font-weight: 500; color: #94a3b8; letter-spacing: 0.04em; text-transform: uppercase; }

/* ── Feature cards ── */
.features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.5rem;
}
.feature-card {
    background: #fff;
    border: 1px solid #e8e4de;
    border-radius: 14px;
    padding: 1.2rem 1.1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.feature-icon { font-size: 1.3rem; margin-bottom: 0.5rem; }
.feature-title { font-size: 0.85rem; font-weight: 600; color: #1e293b; margin-bottom: 0.3rem; }
.feature-desc { font-size: 0.76rem; color: #94a3b8; line-height: 1.5; }

/* ── Primary CTA button ── */
.stButton > button {
    background: #2563eb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2rem !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 2px 12px rgba(37,99,235,0.25) !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #1d4ed8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.32) !important;
}

/* ── Chat header ── */
.chat-header {
    padding: 1.6rem 0 0.8rem;
    border-bottom: 1px solid #e8e4de;
    margin-bottom: 1.4rem;
}
.chat-title {
    font-family: 'Lora', serif;
    font-size: 1.55rem;
    font-weight: 600;
    color: #0f172a;
    margin: 0 0 0.2rem;
    letter-spacing: -0.02em;
}
.chat-sub { font-size: 0.83rem; color: #94a3b8; }

/* ── Suggestion chips override ── */
div[data-testid="column"] .stButton > button {
    background: #fff !important;
    color: #374151 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 999px !important;
    font-size: 0.79rem !important;
    font-weight: 400 !important;
    padding: 0.42rem 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    text-align: left !important;
    width: auto !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #eef2ff !important;
    border-color: #c7d7fd !important;
    color: #2563eb !important;
    transform: none !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.12) !important;
}

/* ── Message bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
.msg-user .bubble {
    background: #2563eb;
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1.1rem;
    max-width: 80%;
    font-size: 0.91rem;
    line-height: 1.6;
    box-shadow: 0 2px 10px rgba(37,99,235,0.22);
}
.msg-bot {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
    gap: 0.55rem;
    align-items: flex-start;
}
.bot-avatar {
    width: 30px; height: 30px;
    background: #eef2ff;
    border: 1px solid #c7d7fd;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
    margin-top: 3px;
}
.msg-bot .bubble {
    background: #fff;
    border: 1px solid #e8e4de;
    color: #1e293b;
    border-radius: 4px 18px 18px 18px;
    padding: 0.85rem 1.1rem;
    max-width: 84%;
    font-size: 0.91rem;
    line-height: 1.7;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.msg-bot .bubble .meta {
    font-size: 0.68rem;
    color: #94a3b8;
    margin-top: 0.5rem;
    border-top: 1px solid #f1f5f9;
    padding-top: 0.4rem;
}
.msg-error .bubble {
    background: #fef2f2 !important;
    border-color: #fecaca !important;
    color: #dc2626 !important;
}

/* ── Disclaimer ── */
.disclaimer {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.77rem;
    color: #92400e;
    margin-bottom: 1.2rem;
    line-height: 1.55;
}

/* ── Text input ── */
.stTextInput > div > div > input {
    background: #fff !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 12px !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 0.92rem !important;
    color: #1e293b !important;
    padding: 0.78rem 1rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #cbd5e1 !important; }
.stTextInput label { display: none !important; }

/* ── Send button override ── */
.send-wrap .stButton > button {
    background: #2563eb !important;
    border-radius: 10px !important;
    padding: 0.78rem 1.2rem !important;
    font-size: 0.95rem !important;
    width: 100% !important;
}

/* ── Back button override ── */
.back-wrap .stButton > button {
    background: transparent !important;
    color: #64748b !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    padding: 0.38rem 0.85rem !important;
    box-shadow: none !important;
    width: auto !important;
}
.back-wrap .stButton > button:hover {
    background: #f8fafc !important;
    transform: none !important;
}

/* ── Footer ── */
.site-footer {
    text-align: center;
    padding-top: 2rem;
    color: #cbd5e1;
    font-size: 0.72rem;
    border-top: 1px solid #e8e4de;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_home():
    st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">💹 FundFacts<span class="dot">.</span></div>
        <div class="navbar-pill">HDFC AMC · Facts Only</div>
    </div>

    <div class="hero">
        <div class="hero-tag"><span class="green-dot"></span>&nbsp;Official sources only · No investment advice</div>
        <h1 class="hero-title">Instant answers to<br><span class="accent">Mutual Fund questions</span></h1>
        <p class="hero-desc">
            Expense ratios, exit loads, SIP minimums, ELSS lock-ins —
            sourced directly from HDFC AMC, SEBI, and AMFI documents.
            Every answer includes a citation link.
        </p>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-val blue">15+</div>
            <div class="stat-lbl">Official Sources</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">100%</div>
            <div class="stat-lbl">Cited Answers</div>
        </div>
        <div class="stat-card">
            <div class="stat-val">₹500</div>
            <div class="stat-lbl">Min SIP (HDFC)</div>
        </div>
        <div class="stat-card">
            <div class="stat-val blue">3 yrs</div>
            <div class="stat-lbl">ELSS Lock-in</div>
        </div>
    </div>

    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Expense Ratios</div>
            <div class="feature-desc">Exact ratios from official HDFC AMC fact sheets — no guesswork.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">ELSS Lock-ins</div>
            <div class="feature-desc">Lock-in periods and tax-saving eligibility with SEBI citations.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💸</div>
            <div class="feature-title">SIP Minimums</div>
            <div class="feature-desc">Minimum SIP and lumpsum thresholds straight from fund documents.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🚪</div>
            <div class="feature-title">Exit Loads</div>
            <div class="feature-desc">Redemption charges and applicable timeframes, source-backed.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Statements</div>
            <div class="feature-desc">Step-by-step guides for CAS and capital gains downloads.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Transparent</div>
            <div class="feature-desc">If we don't have the data, we say so. No hallucinations.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.2, 2, 1.2])
    with col2:
        if st.button("Ask a question →", key="cta_btn"):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("""
    <div class="site-footer">
        Data from HDFC AMC · AMFI · SEBI · Groww &nbsp;·&nbsp; Facts only · No investment advice · No PII stored
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# CHAT PAGE
# ════════════════════════════════════════════════════════════════════════════
SUGGESTIONS = [
    ("📊  Expense ratio — HDFC Top 100", "What is the expense ratio of HDFC Top 100 Fund?"),
    ("🔒  ELSS lock-in period", "What is the lock-in period for HDFC ELSS Tax Saver Fund?"),
    ("📄  Download capital gains statement", "How do I download capital gains statement from HDFC AMC?"),
    ("💸  Minimum SIP — HDFC Flexi Cap", "What is the minimum SIP amount for HDFC Flexi Cap Fund?"),
    ("🚪  Exit load — Balanced Advantage", "What is the exit load for HDFC Balanced Advantage Fund?"),
    ("📈  Benchmark — HDFC Flexi Cap", "What is the benchmark index for HDFC Flexi Cap Fund?"),
]

def call_api(question: str) -> str:
    r = requests.post(API_URL, json={"question": question}, timeout=30)
    r.raise_for_status()
    return r.json()["answer"]

def render_chat():
    # Back button
    st.markdown('<div class="back-wrap">', unsafe_allow_html=True)
    col_b, _ = st.columns([1, 6])
    with col_b:
        if st.button("← Back", key="back_btn"):
            st.session_state.page = "home"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="chat-header">
        <div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.25rem;">
            <span style="font-size:1.3rem;">💹</span>
            <div class="chat-title">FundFacts</div>
            <span style="background:#dcfce7;color:#16a34a;font-size:0.65rem;font-weight:600;
                padding:0.18rem 0.55rem;border-radius:999px;letter-spacing:0.06em;text-transform:uppercase;">
                Online
            </span>
        </div>
        <div class="chat-sub">Ask about HDFC mutual funds · Expense ratios, exit loads, SIP minimums &amp; more</div>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Facts-only assistant.</strong> Provides factual information from official HDFC AMC,
        SEBI &amp; AMFI documents only. Not investment advice. Verify with official sources before any decision.
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips — shown only when chat is empty
    if not st.session_state.messages:
        st.markdown("""
        <p style="font-size:0.7rem;font-weight:600;letter-spacing:0.1em;
            text-transform:uppercase;color:#94a3b8;margin-bottom:0.6rem;">
            Try a question
        </p>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for i, (label, query) in enumerate(SUGGESTIONS):
            with (col1 if i % 2 == 0 else col2):
                if st.button(label, key=f"chip_{i}"):
                    st.session_state.pending_query = query
                    st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # Render history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-user">
                <div class="bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            err_class = "msg-error" if msg.get("status") == "error" else ""
            st.markdown(f"""
            <div class="msg-bot {err_class}">
                <div class="bot-avatar">💹</div>
                <div class="bubble">
                    {msg["content"]}
                    <div class="meta">Last updated from sources: HDFC AMC · AMFI · SEBI</div>
                </div>
            </div>""", unsafe_allow_html=True)

    # Handle chip-triggered query
    if st.session_state.pending_query:
        q = st.session_state.pending_query
        st.session_state.pending_query = ""
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("Looking up official sources…"):
            try:
                ans = call_api(q)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Could not fetch an answer — {str(e)}",
                    "status": "error",
                })
        st.rerun()

    # Input row
    st.markdown("<br>", unsafe_allow_html=True)
    inp_col, btn_col = st.columns([5, 1])
    with inp_col:
        user_input = st.text_input(
            "q", value="", key="chat_input",
            placeholder="Ask about expense ratios, exit loads, SIP minimums…",
            label_visibility="collapsed",
        )
    with btn_col:
        st.markdown('<div class="send-wrap">', unsafe_allow_html=True)
        send = st.button("Send ↵", key="send_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        q = user_input.strip()
        st.session_state.messages.append({"role": "user", "content": q})
        with st.spinner("Looking up official sources…"):
            try:
                ans = call_api(q)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Could not fetch an answer — {str(e)}",
                    "status": "error",
                })
        st.rerun()

    st.markdown("""
    <div class="site-footer">
        Data from HDFC AMC · AMFI · SEBI &nbsp;·&nbsp; Facts only · No investment advice
    </div>
    """, unsafe_allow_html=True)


# ─── Router ──────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
else:
    render_chat()