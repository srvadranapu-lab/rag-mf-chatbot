import streamlit as st
import requests

st.set_page_config(
    page_title="Groww – MF FAQ Assistant",
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
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ─── Theme toggle ────────────────────────────────────────────────────────────
dark = st.session_state.dark_mode

# ─── Global CSS ──────────────────────────────────────────────────────────────
theme_vars = """
    --bg:           #0d1117;
    --bg2:          #161b22;
    --bg3:          #1c2128;
    --border:       #30363d;
    --text:         #e6edf3;
    --text-muted:   #7d8590;
    --text-strong:  #f0f6fc;
    --accent:       #00c853;
    --accent-hover: #00e676;
    --blue:         #2563eb;
    --pill-bg:      rgba(0,200,83,0.12);
    --pill-color:   #00c853;
    --pill-border:  rgba(0,200,83,0.25);
    --card-shadow:  0 2px 12px rgba(0,0,0,0.4);
    --bubble-user-bg: #2563eb;
    --bubble-bot-bg:  #1c2128;
    --bubble-bot-text:#e6edf3;
    --input-bg:     #161b22;
    --footer-color: #30363d;
    --tag-bg:       rgba(0,200,83,0.1);
    --tag-border:   rgba(0,200,83,0.2);
    --tag-color:    #7d8590;
    --disc-bg:      rgba(255,200,0,0.07);
    --disc-border:  rgba(255,200,0,0.18);
    --disc-color:   #b8860b;
""" if dark else """
    --bg:           #f7f9f7;
    --bg2:          #ffffff;
    --bg3:          #f0f7f0;
    --border:       #e2e8e2;
    --text:         #1a2e1a;
    --text-muted:   #6b7c6b;
    --text-strong:  #0d1f0d;
    --accent:       #00b341;
    --accent-hover: #009933;
    --blue:         #2563eb;
    --pill-bg:      #e8f5e9;
    --pill-color:   #00b341;
    --pill-border:  #b2dfdb;
    --card-shadow:  0 1px 4px rgba(0,0,0,0.06);
    --bubble-user-bg: #2563eb;
    --bubble-bot-bg:  #ffffff;
    --bubble-bot-text:#1a2e1a;
    --input-bg:     #ffffff;
    --footer-color: #b2c2b2;
    --tag-bg:       #f0faf0;
    --tag-border:   #c8e6c9;
    --tag-color:    #6b7c6b;
    --disc-bg:      #fffde7;
    --disc-border:  #ffe082;
    --disc-color:   #795548;
"""

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

:root {{
    {theme_vars}
}}

html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif;
    color: var(--text);
}}

.stApp {{
    background: var(--bg);
    min-height: 100vh;
    transition: background 0.3s ease, color 0.3s ease;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.block-container {{
    padding-top: 0 !important;
    padding-bottom: 4rem !important;
    max-width: 800px !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
}}

/* ── Navbar ── */
.navbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.4rem 0 1rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}}
.navbar-brand {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.04em;
    font-family: 'Sora', sans-serif;
    line-height: 1;
}}
.navbar-right {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}
.navbar-pill {{
    background: var(--pill-bg);
    color: var(--pill-color);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    border: 1px solid var(--pill-border);
    white-space: nowrap;
}}
.theme-toggle {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
    flex-shrink: 0;
}}

/* ── Hero ── */
.hero {{
    padding: 3.5rem 0 2.2rem;
    text-align: center;
}}
.hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--tag-bg);
    border: 1px solid var(--tag-border);
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--tag-color);
    padding: 0.32rem 1rem;
    margin-bottom: 1.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}}
.hero-tag .green-dot {{
    width: 7px; height: 7px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 3px rgba(0,179,65,0.2);
}}
.hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 5.5vw, 3.2rem);
    font-weight: 400;
    color: var(--text-strong);
    line-height: 1.18;
    letter-spacing: -0.01em;
    margin: 0 0 1.2rem;
}}
.hero-title .accent {{ font-style: italic; color: var(--accent); }}
.hero-title .underline-word {{
    position: relative;
    display: inline-block;
}}
.hero-title .underline-word::after {{
    content: '';
    position: absolute;
    bottom: 2px; left: 0;
    width: 100%; height: 3px;
    background: var(--accent);
    border-radius: 2px;
    opacity: 0.5;
}}
.hero-desc {{
    color: var(--text-muted);
    font-size: 0.96rem;
    font-weight: 400;
    line-height: 1.75;
    max-width: 530px;
    margin: 0 auto 2rem;
}}

/* ── CTA button (hero) ── */
.cta-wrapper {{
    display: flex;
    justify-content: center;
    margin-bottom: 2.8rem;
}}
.stButton > button {{
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 2.2rem !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 3px 16px rgba(0,179,65,0.3) !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button:hover {{
    background: var(--accent-hover) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,179,65,0.38) !important;
}}

/* ── Stats row ── */
.stats-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.5rem;
}}
.stat-card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    box-shadow: var(--card-shadow);
    transition: transform 0.18s, box-shadow 0.18s;
}}
.stat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}}
.stat-val {{
    font-size: 1.4rem; font-weight: 800;
    color: var(--text-strong);
    letter-spacing: -0.04em;
    margin-bottom: 0.25rem;
    font-family: 'Sora', sans-serif;
}}
.stat-val.green {{ color: var(--accent); }}
.stat-lbl {{ font-size: 0.67rem; font-weight: 600; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase; }}

/* ── Feature cards ── */
.features-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.5rem;
}}
.feature-card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.3rem 1.15rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.18s, box-shadow 0.18s;
}}
.feature-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.09);
}}
.feature-icon {{ font-size: 1.4rem; margin-bottom: 0.55rem; }}
.feature-title {{ font-size: 0.84rem; font-weight: 700; color: var(--text-strong); margin-bottom: 0.3rem; }}
.feature-desc {{ font-size: 0.75rem; color: var(--text-muted); line-height: 1.55; }}

/* ── Trust strip ── */
.trust-strip {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    padding: 1rem 0 2rem;
    border-top: 1px solid var(--border);
    flex-wrap: wrap;
}}
.trust-item {{
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}}
.trust-dot {{
    width: 5px; height: 5px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
}}

/* ── Chat header ── */
.chat-header {{
    padding: 1.6rem 0 0.9rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}}
.chat-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: var(--text-strong);
    margin: 0 0 0.2rem;
    letter-spacing: -0.01em;
}}
.chat-sub {{ font-size: 0.82rem; color: var(--text-muted); }}

/* ── Suggestion chips ── */
div[data-testid="column"] .stButton > button {{
    background: var(--bg2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.44rem 1rem !important;
    box-shadow: var(--card-shadow) !important;
    text-align: left !important;
    width: auto !important;
    letter-spacing: 0 !important;
}}
div[data-testid="column"] .stButton > button:hover {{
    background: var(--bg3) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: 0 2px 10px rgba(0,179,65,0.15) !important;
}}

/* ── Message bubbles ── */
.msg-user {{
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}}
.msg-user .bubble {{
    background: var(--bubble-user-bg);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.15rem;
    max-width: 78%;
    font-size: 0.9rem;
    line-height: 1.65;
    box-shadow: 0 2px 12px rgba(37,99,235,0.25);
}}
.msg-bot {{
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
    gap: 0.55rem;
    align-items: flex-start;
}}
.msg-error .bubble {{
    border-left: 3px solid #ef4444 !important;
}}
.bot-avatar {{
    width: 32px; height: 32px;
    background: var(--pill-bg);
    border: 1px solid var(--pill-border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
    margin-top: 3px;
}}
.msg-bot .bubble {{
    background: var(--bubble-bot-bg);
    color: var(--bubble-bot-text);
    border: 1px solid var(--border);
    border-radius: 4px 18px 18px 18px;
    padding: 0.8rem 1.15rem;
    max-width: 78%;
    font-size: 0.9rem;
    line-height: 1.7;
    box-shadow: var(--card-shadow);
}}
.meta {{
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-top: 0.55rem;
    font-family: 'DM Mono', monospace;
}}

/* ── Disclaimer ── */
.disclaimer {{
    background: var(--disc-bg);
    border: 1px solid var(--disc-border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    color: var(--disc-color);
    margin-bottom: 1.2rem;
    line-height: 1.55;
}}

/* ── Input / send ── */
.stTextInput input {{
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1rem !important;
}}
.stTextInput input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,179,65,0.15) !important;
}}
.send-wrap .stButton > button {{
    padding: 0.7rem 1rem !important;
    font-size: 0.88rem !important;
    border-radius: 10px !important;
}}

.back-wrap .stButton > button {{
    background: var(--bg2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 0.9rem !important;
    box-shadow: none !important;
    width: auto !important;
}}
.back-wrap .stButton > button:hover {{
    background: var(--bg3) !important;
    transform: none !important;
}}

/* ── Footer ── */
.site-footer {{
    text-align: center;
    padding-top: 2rem;
    color: var(--footer-color);
    font-size: 0.7rem;
    border-top: 1px solid var(--border);
    margin-top: 1.5rem;
    letter-spacing: 0.02em;
}}

/* ── Responsive ── */
@media (max-width: 640px) {{
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
    .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .navbar-brand {{ font-size: 1.6rem; }}
    .hero {{ padding: 2rem 0 1.5rem; }}
    .trust-strip {{ gap: 1rem; }}
}}
@media (max-width: 400px) {{
    .features-grid {{ grid-template-columns: 1fr; }}
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
    .block-container {{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════════════════
def render_home():
    moon_or_sun = "☀️" if dark else "🌙"
    title = "Turn off the lights" if not dark else "Turn on the lights"

    st.markdown(f"""
    <div class="navbar">
        <div class="navbar-brand">Groww</div>
        <div class="navbar-right">
            <div class="navbar-pill">HDFC AMC · Facts Only</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle button — rendered as Streamlit button to capture click
    col_space, col_toggle = st.columns([9, 1])
    with col_toggle:
        if st.button(moon_or_sun, key="theme_home", help=title):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("""
    <div class="hero">
        <div class="hero-tag"><span class="green-dot"></span>&nbsp;Official sources only · No investment advice</div>
        <h1 class="hero-title">
            Stop guessing.<br>
            Get <span class="accent">fund facts</span> you can<br>
            <span class="underline-word">actually trust</span>.
        </h1>
        <p class="hero-desc">
            Expense ratios, exit loads, SIP minimums, ELSS lock-ins —
            sourced directly from HDFC AMC, SEBI, and AMFI documents.
            Every answer includes a citation link.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA button right below the description
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Ask a question →", key="cta_btn"):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("""
    <div class="stats-row" style="margin-top:2.5rem;">
        <div class="stat-card">
            <div class="stat-val green">15+</div>
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
            <div class="stat-val green">3 yrs</div>
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
            <div class="feature-title">Zero Hallucinations</div>
            <div class="feature-desc">If we don't have the data, we say so. No made-up figures.</div>
        </div>
    </div>

    <div class="trust-strip">
        <span class="trust-item"><span class="trust-dot"></span> HDFC AMC Verified</span>
        <span class="trust-item"><span class="trust-dot"></span> SEBI Registered</span>
        <span class="trust-item"><span class="trust-dot"></span> AMFI Data</span>
        <span class="trust-item"><span class="trust-dot"></span> No PII Stored</span>
        <span class="trust-item"><span class="trust-dot"></span> Facts Only</span>
    </div>

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
    moon_or_sun = "☀️" if dark else "🌙"

    # Navbar with theme toggle
    st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">Groww</div>
        <div class="navbar-right">
            <div class="navbar-pill">HDFC AMC · Facts Only</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_col, toggle_col = st.columns([9, 1])
    with toggle_col:
        if st.button(moon_or_sun, key="theme_chat"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

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
            <div class="chat-title">Fund Facts</div>
            <span style="background:#dcfce7;color:#16a34a;font-size:0.65rem;font-weight:700;
                padding:0.18rem 0.6rem;border-radius:999px;letter-spacing:0.06em;text-transform:uppercase;">
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
        <p style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;
            text-transform:uppercase;color:var(--text-muted);margin-bottom:0.6rem;">
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
                <div class="bot-avatar">🌱</div>
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
        Data from HDFC AMC · AMFI · SEBI &nbsp;·&nbsp; Facts only · No investment advice · No PII stored
    </div>
    """, unsafe_allow_html=True)


# ─── Router ──────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
else:
    render_chat()