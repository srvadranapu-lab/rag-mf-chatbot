import streamlit as st
import requests

st.set_page_config(
    page_title="Groww – MF FAQ Assistant",
    layout="centered",
    page_icon="💹",
    initial_sidebar_state="collapsed",
)

API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ─── Session state defaults ───────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.session_state.dark_mode
moon_or_sun = "☀️" if dark else "🌙"

# ─── Theme variables ──────────────────────────────────────────────────────────
theme_vars = """
    --bg:             #0d1117;
    --bg2:            #161b22;
    --bg3:            #1c2128;
    --border:         #30363d;
    --text:           #e6edf3;
    --text-muted:     #7d8590;
    --text-strong:    #f0f6fc;
    --accent:         #00c853;
    --accent-hover:   #00e676;
    --pill-bg:        rgba(0,200,83,0.12);
    --pill-color:     #00c853;
    --pill-border:    rgba(0,200,83,0.25);
    --card-shadow:    0 2px 12px rgba(0,0,0,0.4);
    --bubble-user-bg: #2563eb;
    --bubble-bot-bg:  #1c2128;
    --bubble-bot-text:#e6edf3;
    --input-bg:       #161b22;
    --footer-color:   #30363d;
    --tag-bg:         rgba(0,200,83,0.1);
    --tag-border:     rgba(0,200,83,0.2);
    --tag-color:      #7d8590;
    --disc-bg:        rgba(255,200,0,0.07);
    --disc-border:    rgba(255,200,0,0.18);
    --disc-color:     #cca300;
""" if dark else """
    --bg:             #f7f9f7;
    --bg2:            #ffffff;
    --bg3:            #f0f7f0;
    --border:         #e2e8e2;
    --text:           #1a2e1a;
    --text-muted:     #6b7c6b;
    --text-strong:    #0d1f0d;
    --accent:         #00b341;
    --accent-hover:   #009933;
    --pill-bg:        #e8f5e9;
    --pill-color:     #00b341;
    --pill-border:    #b2dfdb;
    --card-shadow:    0 1px 4px rgba(0,0,0,0.06);
    --bubble-user-bg: #2563eb;
    --bubble-bot-bg:  #ffffff;
    --bubble-bot-text:#1a2e1a;
    --input-bg:       #ffffff;
    --footer-color:   #b2c2b2;
    --tag-bg:         #f0faf0;
    --tag-border:     #c8e6c9;
    --tag-color:      #6b7c6b;
    --disc-bg:        #fffde7;
    --disc-border:    #ffe082;
    --disc-color:     #795548;
"""

# ─── Global CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&display=swap');

:root {{ {theme_vars} }}

html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif;
    color: var(--text);
}}
.stApp {{
    background: var(--bg);
    min-height: 100vh;
    transition: background 0.3s ease;
}}
#MainMenu, footer, header {{ visibility: hidden; }}

/* Page container — full-width, auto margins */
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 4rem !important;
    max-width: 820px !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
    box-sizing: border-box !important;
    width: 100% !important;
}}

/* ══ NAVBAR ROW (rendered as st.columns) ════════════════════════════════════ */
/* Left col: brand + pill */
.nav-left {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.3rem 0 1rem;
    width: 100%;
    box-sizing: border-box;
}}
.nav-right-group {{
    display: flex;
    align-items: center;
    gap: 0.65rem;
}}
.nav-brand {{
    font-size: 2rem;
    font-weight: 800;
    color: var(--accent);
    font-family: 'Sora', sans-serif;
    letter-spacing: -0.04em;
    line-height: 1;
    flex-shrink: 0;
}}
.nav-pill {{
    background: var(--pill-bg);
    color: var(--pill-color);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 0.28rem 0.8rem;
    border-radius: 999px;
    border: 1px solid var(--pill-border);
    white-space: nowrap;
}}
.nav-icon-btn {{
    background: var(--bg2);
    color: var(--text);
    border: 1.5px solid var(--border);
    border-radius: 50%;
    width: 34px;
    height: 34px;
    min-width: 34px;
    font-size: 1rem;
    line-height: 1;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color 0.2s, background 0.2s;
    flex-shrink: 0;
    padding: 0;
    margin-left: 0.5rem;
}}
.nav-icon-btn:hover {{
    border-color: var(--accent);
    background: var(--bg3);
}}
/* Navbar wrapper — full width with border-bottom */
.nav-wrapper {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.3rem 0 1rem;
    border-bottom: 1px solid var(--border);
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 0;
}}
/* Right col: toggle button */
.nav-right {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 1.3rem 0 1rem;
    width: 100%;
    box-sizing: border-box;
}}


/* ══ HERO ════════════════════════════════════════════════════════════════════ */
.hero {{
    padding: 3.2rem 0 1.8rem;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}}
.hero-tag {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: var(--tag-bg);
    border: 1px solid var(--tag-border);
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 500;
    color: var(--tag-color);
    padding: 0.3rem 1rem;
    margin-bottom: 1.5rem;
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
    font-size: clamp(2rem, 5.5vw, 3.1rem);
    font-weight: 400;
    color: var(--text-strong);
    line-height: 1.22;
    letter-spacing: -0.01em;
    margin: 0 0 1.1rem;
    text-align: center;
}}
.stop-guess {{
    display: block;
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    font-size: clamp(1.2rem, 3.2vw, 1.6rem);
    letter-spacing: 0.2em;
    color: var(--accent);
    margin-bottom: 0.4rem;
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
    opacity: 0.45;
}}
.hero-desc {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.75;
    max-width: 520px;
    margin: 0 auto 1.8rem auto;
    text-align: center;
    display: block;
    width: 100%;
}}

/* ══ CTA BUTTON — centered ═══════════════════════════════════════════════════ */
.cta-center-wrap {{
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
}}
.cta-center-wrap .stButton > button {{
    width: auto !important;
    padding: 0.78rem 2.4rem !important;
}}

/* ══ NAVBAR ICON BUTTON (theme toggle beside pill) ═══════════════════════════ */
.nav-icon-wrap {{ display: flex; align-items: center; justify-content: flex-end; padding-top: 1rem; }}
.nav-icon-wrap .stButton > button {{
    background: var(--bg2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 50% !important;
    width: 34px !important;
    height: 34px !important;
    min-width: 34px !important;
    min-height: 34px !important;
    font-size: 1rem !important;
    padding: 0 !important;
    box-shadow: none !important;
    transform: none !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}}
.nav-icon-wrap .stButton > button:hover {{
    border-color: var(--accent) !important;
    background: var(--bg3) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ══ ALL BUTTONS — base green ════════════════════════════════════════════════ */
.stButton > button {{
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.78rem 2rem !important;
    transition: background 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 3px 16px rgba(0,179,65,0.28) !important;
    width: 100% !important;
    letter-spacing: 0.01em !important;
}}
.stButton > button:hover {{
    background: var(--accent-hover) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,179,65,0.36) !important;
}}

/* ══ STATS ROW ═══════════════════════════════════════════════════════════════ */
.stats-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.2rem;
    width: 100%;
}}
.stat-card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    box-shadow: var(--card-shadow);
    transition: transform 0.18s;
}}
.stat-card:hover {{ transform: translateY(-2px); }}
.stat-val {{
    font-size: 1.35rem; font-weight: 800;
    color: var(--text-strong);
    letter-spacing: -0.04em;
    margin-bottom: 0.22rem;
}}
.stat-val.green {{ color: var(--accent); }}
.stat-lbl {{ font-size: 0.66rem; font-weight: 600; color: var(--text-muted); letter-spacing: 0.06em; text-transform: uppercase; }}

/* ══ FEATURE CARDS ═══════════════════════════════════════════════════════════ */
.features-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 2.2rem;
    width: 100%;
}}
.feature-card {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.1rem;
    box-shadow: var(--card-shadow);
    transition: transform 0.18s;
}}
.feature-card:hover {{ transform: translateY(-2px); }}
.feature-icon {{ font-size: 1.35rem; margin-bottom: 0.5rem; }}
.feature-title {{ font-size: 0.83rem; font-weight: 700; color: var(--text-strong); margin-bottom: 0.28rem; }}
.feature-desc {{ font-size: 0.74rem; color: var(--text-muted); line-height: 1.55; }}

/* ══ TRUST STRIP ═════════════════════════════════════════════════════════════ */
.trust-strip {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.4rem;
    padding: 1rem 0 1.8rem;
    border-top: 1px solid var(--border);
    flex-wrap: wrap;
}}
.trust-item {{
    font-size: 0.7rem; font-weight: 600;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    display: flex; align-items: center; gap: 0.32rem;
}}
.trust-dot {{
    width: 5px; height: 5px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
}}

/* ══ BACK BUTTON ════════════════════════════════════════════════════════════ */
.back-wrap {{ display: inline-block; margin-top: 0.8rem; margin-bottom: 0.5rem; }}
.back-wrap .stButton > button {{
    background: var(--bg2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.42rem 0.95rem !important;
    box-shadow: none !important;
    width: auto !important;
    transform: none !important;
    letter-spacing: 0 !important;
}}
.back-wrap .stButton > button:hover {{
    background: var(--bg3) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: none !important;
}}

/* ══ CHAT HEADER ════════════════════════════════════════════════════════════ */
.chat-header {{
    padding: 1.4rem 0 0.85rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.3rem;
}}
.chat-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.55rem;
    font-weight: 400;
    color: var(--text-strong);
    margin: 0 0 0.18rem;
    letter-spacing: -0.01em;
}}
.chat-sub {{ font-size: 0.81rem; color: var(--text-muted); }}

/* ══ SUGGESTION CHIPS ════════════════════════════════════════════════════════ */
div[data-testid="column"] .stButton > button {{
    background: var(--bg2) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 999px !important;
    font-size: 0.77rem !important;
    font-weight: 500 !important;
    padding: 0.42rem 1rem !important;
    box-shadow: var(--card-shadow) !important;
    text-align: left !important;
    width: 100% !important;
    letter-spacing: 0 !important;
    transform: none !important;
}}
div[data-testid="column"] .stButton > button:hover {{
    background: var(--bg3) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: none !important;
    box-shadow: 0 2px 10px rgba(0,179,65,0.12) !important;
}}

/* ══ MESSAGE BUBBLES ═════════════════════════════════════════════════════════ */
.msg-user {{
    display: flex; justify-content: flex-end; margin-bottom: 1rem;
}}
.msg-user .bubble {{
    background: var(--bubble-user-bg); color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.78rem 1.1rem; max-width: 78%;
    font-size: 0.9rem; line-height: 1.65;
    box-shadow: 0 2px 12px rgba(37,99,235,0.22);
}}
.msg-bot {{
    display: flex; justify-content: flex-start;
    margin-bottom: 1rem; gap: 0.5rem; align-items: flex-start;
}}
.msg-error .bubble {{ border-left: 3px solid #ef4444 !important; }}
.bot-avatar {{
    width: 32px; height: 32px;
    background: var(--pill-bg); border: 1px solid var(--pill-border);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0; margin-top: 3px;
}}
.msg-bot .bubble {{
    background: var(--bubble-bot-bg); color: var(--bubble-bot-text);
    border: 1px solid var(--border);
    border-radius: 4px 18px 18px 18px;
    padding: 0.78rem 1.1rem; max-width: 78%;
    font-size: 0.9rem; line-height: 1.7;
    box-shadow: var(--card-shadow);
}}
.meta {{
    font-size: 0.67rem; color: var(--text-muted);
    margin-top: 0.5rem; font-family: 'DM Mono', monospace;
}}

/* ══ DISCLAIMER ══════════════════════════════════════════════════════════════ */
.disclaimer {{
    background: var(--disc-bg);
    border: 1px solid var(--disc-border);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    font-size: 0.77rem; color: var(--disc-color);
    margin-bottom: 1.2rem; line-height: 1.55;
}}

/* ══ TEXT INPUT ═══════════════════════════════════════════════════════════════ */
.stTextInput input {{
    background: var(--input-bg) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
    height: 46px !important;
    padding: 0 1rem !important;
    box-sizing: border-box !important;
}}
.stTextInput input:focus {{
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,179,65,0.13) !important;
    outline: none !important;
}}

/* ══ SEND BUTTON — small circle inline with input ════════════════════════════ */
.send-wrap {{ width: 100%; margin-top: 0; display: flex; align-items: flex-end; }}
.send-wrap .stButton > button {{
    height: 38px !important;
    width: 38px !important;
    min-height: 38px !important;
    min-width: 38px !important;
    padding: 0 !important;
    font-size: 1.05rem !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 8px rgba(0,179,65,0.22) !important;
    transform: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 4px !important;
    margin-top: 0 !important;
}}
.send-wrap .stButton > button:hover {{
    transform: none !important;
    box-shadow: 0 4px 14px rgba(0,179,65,0.34) !important;
}}
/* Align send button column with input — remove label gap */
div[data-testid="stHorizontalBlock"]:has(.send-wrap) {{
    align-items: flex-end !important;
}}



/* ══ FOOTER ══════════════════════════════════════════════════════════════════ */
.site-footer {{
    text-align: center;
    padding-top: 1.8rem;
    color: var(--footer-color);
    font-size: 0.69rem;
    border-top: 1px solid var(--border);
    margin-top: 1.5rem;
    letter-spacing: 0.02em;
    width: 100%;
}}

/* ══ RESPONSIVE ══════════════════════════════════════════════════════════════ */
@media (max-width: 640px) {{
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
    .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .nav-brand {{ font-size: 1.6rem; }}
    .block-container {{
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
}}
@media (max-width: 400px) {{
    .features-grid {{ grid-template-columns: 1fr; }}
    .block-container {{
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
    }}
}}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SHARED NAVBAR
# The brand + pill are pure HTML (left col); the toggle is a Streamlit button
# (right col) so Streamlit can handle the click. A negative margin-top pulls
# the right col up to align with the left col's border-bottom line.
# ═════════════════════════════════════════════════════════════════════════════
def render_navbar(page_key: str):
    icon = "☀️" if dark else "🌙"
    nav_col, btn_col = st.columns([10, 1])
    with nav_col:
        st.markdown(f"""
        <div class="nav-left">
            <span class="nav-brand">Groww</span>
            <div class="nav-right-group">
                <span class="nav-pill">HDFC AMC · Facts Only</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with btn_col:
        st.markdown('<div class="nav-icon-wrap">', unsafe_allow_html=True)
        if st.button(icon, key=f"theme_{page_key}"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<hr style="margin:0;border:none;border-top:1px solid var(--border);width:100%;">', unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═════════════════════════════════════════════════════════════════════════════
def render_home():
    render_navbar("home")

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">
            <span class="green-dot"></span>&nbsp;Official sources only · No investment advice
        </div>
        <h1 class="hero-title">
            <span class="stop-guess">STOP GUESSING</span>
            Get <span class="accent">fund facts</span> you can <span class="underline-word">actually trust</span>.
        </h1>
        <p class="hero-desc">
            Expense ratios, exit loads, SIP minimums, ELSS lock-ins —
            sourced directly from HDFC AMC, SEBI, and AMFI documents.
            Every answer includes a citation link.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA — centred Streamlit button
    st.markdown('<div class="cta-center-wrap">', unsafe_allow_html=True)
    if st.button("Ask a question →", key="cta_btn"):
        st.session_state.page = "chat"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row" style="margin-top:2.4rem;">
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
        Data from HDFC AMC · AMFI · SEBI · Groww &nbsp;·&nbsp;
        Facts only · No investment advice · No PII stored
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# CHAT PAGE
# ═════════════════════════════════════════════════════════════════════════════
SUGGESTIONS = [
    ("📊  Expense ratio — HDFC Top 100",    "What is the expense ratio of HDFC Top 100 Fund?"),
    ("🔒  ELSS lock-in period",              "What is the lock-in period for HDFC ELSS Tax Saver Fund?"),
    ("📄  Download capital gains statement", "How do I download capital gains statement from HDFC AMC?"),
    ("💸  Minimum SIP — HDFC Flexi Cap",    "What is the minimum SIP amount for HDFC Flexi Cap Fund?"),
    ("🚪  Exit load — Balanced Advantage",  "What is the exit load for HDFC Balanced Advantage Fund?"),
    ("📈  Benchmark — HDFC Flexi Cap",      "What is the benchmark index for HDFC Flexi Cap Fund?"),
]

def call_api(question: str) -> str:
    r = requests.post(API_URL, json={"question": question}, timeout=30)
    r.raise_for_status()
    return r.json()["answer"]

def render_chat():
    render_navbar("chat")

    # ── Back button ──────────────────────────────────────────────────────────
    st.markdown('<div class="back-wrap">', unsafe_allow_html=True)
    if st.button("← Back", key="back_btn"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="chat-header">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.2rem;">
            <div class="chat-title">Fund Facts</div>
            <span style="background:#dcfce7;color:#16a34a;font-size:0.63rem;font-weight:700;
                padding:0.16rem 0.55rem;border-radius:999px;letter-spacing:0.06em;
                text-transform:uppercase;">Online</span>
        </div>
        <div class="chat-sub">
            Ask about HDFC mutual funds · Expense ratios, exit loads, SIP minimums &amp; more
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="disclaimer">
        ⚠️ <strong>Facts-only assistant.</strong> Provides factual information from official
        HDFC AMC, SEBI &amp; AMFI documents only. Not investment advice.
        Verify with official sources before any decision.
    </div>
    """, unsafe_allow_html=True)

    # ── Suggestion chips ─────────────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown("""
        <p style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;
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

    # ── Chat history ─────────────────────────────────────────────────────────
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

    # ── Chip-triggered query ─────────────────────────────────────────────────
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

    # ── Input + Send (vertically aligned) ───────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    inp_col, btn_col = st.columns([8, 1])
    with inp_col:
        user_input = st.text_input(
            "q", value="", key="chat_input",
            placeholder="Ask about expense ratios, exit loads, SIP minimums…",
            label_visibility="collapsed",
        )
    with btn_col:
        st.markdown('<div class="send-wrap">', unsafe_allow_html=True)
        send = st.button("↑", key="send_btn")
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
        Data from HDFC AMC · AMFI · SEBI &nbsp;·&nbsp;
        Facts only · No investment advice · No PII stored
    </div>
    """, unsafe_allow_html=True)


# ─── Router ───────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
else:
    render_chat()