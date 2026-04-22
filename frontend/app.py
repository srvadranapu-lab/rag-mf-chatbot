import streamlit as st
import requests

st.set_page_config(page_title="MF FAQ Assistant", layout="centered", initial_sidebar_state="collapsed")

API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ── Theme state ──────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "query" not in st.session_state:
    st.session_state.query = ""

dark = st.session_state.dark_mode

# ── Color tokens ─────────────────────────────────────────────────────────────
if dark:
    BG          = "#0D1F1A"
    BG2         = "#132920"
    CARD_BG     = "#1A3329"
    BORDER      = "#2A5040"
    TEXT        = "#E8F5F0"
    TEXT_MUTED  = "#7EB8A0"
    ACCENT      = "#00D09C"
    ACCENT_DARK = "#00A87D"
    PILL_BG     = "#1A3329"
    STAT_BG     = "#1A3329"
    FOOTER_BG   = "#0D1F1A"
    DIVIDER     = "#2A5040"
else:
    BG          = "#F0FDF8"
    BG2         = "#E6FAF4"
    CARD_BG     = "#FFFFFF"
    BORDER      = "#B2EBD8"
    TEXT        = "#0D2B22"
    TEXT_MUTED  = "#4A8C72"
    ACCENT      = "#00C48C"
    ACCENT_DARK = "#009E72"
    PILL_BG     = "#E0F8EF"
    STAT_BG     = "#F8FFFB"
    FOOTER_BG   = "#E6FAF4"
    DIVIDER     = "#B2EBD8"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

  /* ── Reset & base ── */
  html, body, [data-testid="stAppViewContainer"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif;
  }}
  [data-testid="stAppViewContainer"] > .main > div {{
    padding-top: 0 !important;
  }}
  [data-testid="stHeader"] {{ display: none !important; }}
  [data-testid="stToolbar"] {{ display: none !important; }}
  footer {{ display: none !important; }}
  section[data-testid="stSidebar"] {{ display: none !important; }}

  /* ── Main content block ── */
  .block-container {{
    padding: 0 1rem 3rem 1rem !important;
    max-width: 860px !important;
  }}

  /* ── Streamlit buttons: invisible wrappers for pill buttons ── */
  div[data-testid="stButton"] > button {{
    background: {PILL_BG} !important;
    color: {ACCENT} !important;
    border: 1.5px solid {ACCENT} !important;
    border-radius: 24px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.1rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
    letter-spacing: 0.02em;
  }}
  div[data-testid="stButton"] > button:hover {{
    background: {ACCENT} !important;
    color: #fff !important;
    box-shadow: 0 4px 14px {ACCENT}44 !important;
    transform: translateY(-1px) !important;
  }}

  /* Toggle button override */
  .toggle-btn div[data-testid="stButton"] > button {{
    background: transparent !important;
    border: 2px solid {BORDER} !important;
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    padding: 0 !important;
    font-size: 1rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: {TEXT} !important;
    min-height: unset !important;
    line-height: 1 !important;
  }}
  .toggle-btn div[data-testid="stButton"] > button:hover {{
    background: {ACCENT}22 !important;
    color: {ACCENT} !important;
    transform: none !important;
    box-shadow: none !important;
  }}

  /* ── Text input ── */
  div[data-testid="stTextInput"] input {{
    background: {CARD_BG} !important;
    color: {TEXT} !important;
    border: 2px solid {BORDER} !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease;
  }}
  div[data-testid="stTextInput"] input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {ACCENT}22 !important;
  }}
  div[data-testid="stTextInput"] label {{
    color: {TEXT_MUTED} !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
  }}

  /* ── Success box ── */
  div[data-testid="stAlert"] {{
    background: {CARD_BG} !important;
    border: 1.5px solid {ACCENT}66 !important;
    border-left: 4px solid {ACCENT} !important;
    border-radius: 12px !important;
    color: {TEXT} !important;
  }}

  /* ── Spinner ── */
  div[data-testid="stSpinner"] p {{
    color: {TEXT_MUTED} !important;
    font-family: 'DM Sans', sans-serif !important;
  }}

  /* ── Divider ── */
  hr {{
    border-color: {DIVIDER} !important;
    margin: 0.5rem 0 !important;
  }}

  /* ── Custom components ── */
  .groww-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 0.5rem 1rem 0.5rem;
    background: {BG};
  }}
  .groww-logo {{
    font-family: 'DM Sans', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: {ACCENT};
    letter-spacing: -0.03em;
    line-height: 1;
  }}
  .groww-logo span {{
    color: {ACCENT_DARK};
  }}
  .header-right {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }}
  .badge-pill {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 0.35rem 0.85rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    color: {TEXT_MUTED};
    letter-spacing: 0.04em;
    background: transparent;
    white-space: nowrap;
  }}

  .hero-section {{
    text-align: center;
    padding: 3.2rem 1rem 1.8rem 1rem;
  }}
  .hero-eyebrow {{
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    color: {ACCENT};
    text-transform: uppercase;
    margin-bottom: 0.9rem;
  }}
  .hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(3rem, 9vw, 5.2rem);
    font-weight: 400;
    color: {TEXT};
    line-height: 1.0;
    letter-spacing: -0.02em;
    margin: 0 0 0.6rem 0;
    text-transform: uppercase;
  }}
  .hero-title .accent {{
    color: {ACCENT};
    font-style: italic;
  }}
  .hero-subtitle {{
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 500;
    color: {TEXT};
    margin-bottom: 0.9rem;
  }}
  .hero-desc {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: {TEXT_MUTED};
    max-width: 560px;
    margin: 0 auto 2rem auto;
    line-height: 1.7;
  }}

  .pills-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    justify-content: center;
    margin-bottom: 2.8rem;
  }}

  .stats-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 0.5rem 0 2.8rem 0;
  }}
  @media (max-width: 600px) {{
    .stats-row {{ grid-template-columns: repeat(2, 1fr); }}
  }}
  .stat-box {{
    background: {STAT_BG};
    border: 1.5px solid {BORDER};
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
  }}
  .stat-num {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: {ACCENT};
    line-height: 1.1;
  }}
  .stat-label {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    color: {TEXT_MUTED};
    margin-top: 0.2rem;
    font-weight: 500;
    letter-spacing: 0.02em;
  }}

  .section-label {{
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    color: {TEXT_MUTED};
    text-transform: uppercase;
    margin-bottom: 1.2rem;
  }}

  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 0.4rem 0 2.8rem 0;
  }}
  @media (max-width: 500px) {{
    .cards-grid {{ grid-template-columns: 1fr; }}
  }}
  .feature-card {{
    background: {CARD_BG};
    border: 1.5px solid {BORDER};
    border-radius: 14px;
    padding: 1.35rem 1.2rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    cursor: default;
  }}
  .feature-card:hover {{
    transform: translateY(-3px);
    border-color: {ACCENT}88;
    box-shadow: 0 8px 24px {ACCENT}18;
  }}
  .card-icon {{
    font-size: 1.6rem;
    margin-bottom: 0.65rem;
    display: block;
  }}
  .card-title {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 0.35rem;
  }}
  .card-desc {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    color: {TEXT_MUTED};
    line-height: 1.55;
  }}

  .ask-section {{
    background: {BG2};
    border: 1.5px solid {BORDER};
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    margin-bottom: 2.8rem;
  }}
  .ask-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: {TEXT};
    margin-bottom: 0.2rem;
    font-style: italic;
  }}
  .ask-sub {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    color: {TEXT_MUTED};
    margin-bottom: 1.1rem;
  }}
  .answer-header {{
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    color: {ACCENT};
    text-transform: uppercase;
    margin: 1.2rem 0 0.5rem 0;
  }}

  .footer-strip {{
    background: {FOOTER_BG};
    border-top: 1.5px solid {DIVIDER};
    padding: 1.1rem 0;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: {TEXT_MUTED};
    text-transform: uppercase;
  }}
  .footer-dot {{
    color: {ACCENT};
    margin: 0 0.35rem;
  }}
  .footer-bottom {{
    text-align: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    color: {TEXT_MUTED};
    padding: 0.8rem 0 0.3rem 0;
    opacity: 0.8;
  }}
</style>
""", unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
header_left, header_right_col = st.columns([5, 1])

with header_left:
    st.markdown(f"""
    <div class="groww-header" style="padding-right:0">
      <div class="groww-logo">grow<span>w</span></div>
      <div class="header-right">
        <div class="badge-pill">HDFC AMC · Facts Only</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with header_right_col:
    st.markdown('<div style="padding-top:0.9rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
    toggle_icon = "☀️" if dark else "🌙"
    if st.button(toggle_icon, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
  <div class="hero-eyebrow">Mutual Fund Intelligence · India</div>
  <h1 class="hero-title">STOP <span class="accent">Guessing</span></h1>
  <p class="hero-subtitle">Get fund facts you can actually trust</p>
  <p class="hero-desc">
    Expense ratios, exit loads, SIP minimums, ELSS lock-ins — sourced directly
    from HDFC AMC, SEBI, and AMFI documents. Every answer includes a citation link.
  </p>
</div>
""", unsafe_allow_html=True)

# ── SAMPLE QUESTION PILLS ─────────────────────────────────────────────────────
st.markdown('<div class="pills-row">', unsafe_allow_html=True)

pill_cols = st.columns(4)
sample_questions = [
    ("📊 Expense ratio", "What is expense ratio of HDFC Top 100 Fund?"),
    ("🔒 ELSS lock-in",  "What is ELSS lock-in period?"),
    ("📄 Download statement", "How to download mutual fund statement?"),
    ("💸 Exit load",     "What is exit load of HDFC Balanced Advantage Fund?"),
]
for i, (label, question) in enumerate(sample_questions):
    with pill_cols[i]:
        if st.button(label, key=f"pill_{i}"):
            st.session_state.query = question
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── STATS ROW ─────────────────────────────────────────────────────────────────
stats = [
    ("15+",   "Official Sources"),
    ("100%",  "Cited Answers"),
    ("₹500",  "Min SIP (HDFC)"),
    ("3 yrs", "ELSS Lock-in"),
]
st.markdown('<div class="stats-row">', unsafe_allow_html=True)
for num, label in stats:
    st.markdown(f"""
    <div class="stat-box">
      <div class="stat-num">{num}</div>
      <div class="stat-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── FEATURE CARDS ─────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-label">What you can ask</div>', unsafe_allow_html=True)

cards = [
    ("📈", "Expense Ratios",
     "Exact ratios from official HDFC AMC fact sheets — no guesswork."),
    ("🔒", "ELSS Lock-ins",
     "Lock-in periods and tax-saving eligibility with SEBI citations."),
    ("💰", "SIP Minimums",
     "Minimum SIP and lumpsum thresholds straight from fund documents."),
    ("🚪", "Exit Loads",
     "Redemption charges and applicable timeframes, source-backed."),
    ("📋", "Statements",
     "Step-by-step guides for CAS and capital gains downloads."),
    ("🛡️", "Zero Hallucinations",
     "If data is unavailable, explicitly say so. No fabricated answers."),
]

st.markdown('<div class="cards-grid">', unsafe_allow_html=True)
for icon, title, desc in cards:
    st.markdown(f"""
    <div class="feature-card">
      <span class="card-icon">{icon}</span>
      <div class="card-title">{title}</div>
      <div class="card-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── ASK SECTION ───────────────────────────────────────────────────────────────
st.markdown('<div class="ask-section">', unsafe_allow_html=True)
st.markdown(f'<div class="ask-title">Ask anything about your fund</div>', unsafe_allow_html=True)
st.markdown(f'<div class="ask-sub">Powered by RAG · Answers backed by official sources</div>', unsafe_allow_html=True)

query = st.text_input(
    "YOUR QUESTION",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What is the expense ratio of HDFC Flexi Cap Fund?",
    key="main_input",
)

if query:
    with st.spinner("Fetching answer from official sources…"):
        try:
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()
            answer = response.json()["answer"]
        except Exception as e:
            answer = f"Error: {str(e)}"

    st.markdown('<div class="answer-header">▸ Answer</div>', unsafe_allow_html=True)
    st.success(answer)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-strip">
  <span>HDFC AMC Verified</span>
  <span class="footer-dot">·</span>
  <span>SEBI Registered</span>
  <span class="footer-dot">·</span>
  <span>AMFI Data</span>
  <span class="footer-dot">·</span>
  <span>No PII Stored</span>
  <span class="footer-dot">·</span>
  <span>Facts Only</span>
</div>
<div class="footer-bottom">
  Data from HDFC AMC · AMFI · SEBI · Groww · Facts only · No investment advice · No PII stored
</div>
""", unsafe_allow_html=True)