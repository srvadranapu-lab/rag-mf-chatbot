import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="MF FAQ Assistant – Groww", layout="centered")

# ── Dark / Light mode state ──────────────────────────────────────────────────
# [CHANGED] Initialise dark_mode in session state (default: light)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Toggle callback
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# ── CSS variables driven by theme ────────────────────────────────────────────
# [CHANGED] All colours are CSS-variable-based; swap them by switching one class
dark = st.session_state.dark_mode

THEME = {
    "bg":           "#0f1117" if dark else "#f7faf7",
    "surface":      "#1a1d27" if dark else "#ffffff",
    "surface2":     "#23263a" if dark else "#f0f7f0",
    "border":       "#2e3250" if dark else "#d4e8d4",
    "text":         "#e8eaf6" if dark else "#1a2e1a",
    "subtext":      "#9fa8c7" if dark else "#4a6741",
    "green":        "#00d09c",          # Groww primary green – unchanged
    "green_soft":   "#00d09c22",
    "green_hover":  "#00b386",
    "answer_bg":    "#0d2e24" if dark else "#e8f8f3",
    "answer_border":"#00d09c55",
    "spinner":      "#00d09c",
    "toggle_bg":    "#23263a" if dark else "#e6f4e6",
    "toggle_icon":  "🌙"      if dark else "🌞",
}

# ── Inject global CSS ─────────────────────────────────────────────────────────
# [CHANGED] Full custom stylesheet replacing default Streamlit chrome
st.markdown(f"""
<style>
/* ── Google Font: DM Sans (lightweight, fintech-friendly) ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {THEME["bg"]} !important;
    font-family: 'DM Sans', sans-serif !important;
    color: {THEME["text"]} !important;
}}

/* Hide Streamlit's default header/footer/hamburger */
header[data-testid="stHeader"],
footer,
#MainMenu {{
    visibility: hidden !important;
    height: 0 !important;
}}

/* Remove anchor link icons on headings */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
.css-1jc7ptx, .css-15zrgzn {{ display: none !important; }}

/* Main content width */
[data-testid="stAppViewContainer"] > .main > .block-container {{
    max-width: 760px;
    padding: 0 1.5rem 3rem !important;
}}

/* ── Top navbar ── */
/* [CHANGED] Custom header injected as HTML below */
.mf-navbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 0 14px;
    border-bottom: 1.5px solid {THEME["border"]};
    margin-bottom: 28px;
}}

.mf-logo {{
    font-size: 2rem;
    font-weight: 700;
    color: {THEME["green"]};
    letter-spacing: -0.5px;
}}

.mf-logo span {{
    color: {THEME["text"]};
    font-weight: 400;
    font-size: 0.85rem;
    margin-left: 6px;
    vertical-align: middle;
    opacity: 0.55;
}}

.mf-right {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.mf-badge {{
    font-size: 0.72rem;
    font-weight: 600;
    color: {THEME["green"]};
    border: 1.4px solid {THEME["green"]};
    border-radius: 20px;
    padding: 4px 12px;
    letter-spacing: 0.3px;
    white-space: nowrap;
    user-select: none;
    pointer-events: none;
}}

/* ── Page title area ── */
/* [CHANGED] Replaced st.title() with styled HTML block */
.mf-title {{
    font-size: 1.55rem;
    font-weight: 700;
    color: {THEME["text"]};
    margin-bottom: 4px;
    line-height: 1.25;
}}

.mf-subtitle {{
    font-size: 0.82rem;
    color: {THEME["subtext"]};
    margin-bottom: 22px;
    font-weight: 500;
    letter-spacing: 0.2px;
}}

/* ── Divider ── */
.mf-divider {{
    border: none;
    border-top: 1.5px solid {THEME["border"]};
    margin: 20px 0;
}}

/* ── Example questions label ── */
.mf-section-label {{
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {THEME["subtext"]};
    margin-bottom: 10px;
}}

/* ── Example question buttons ── */
/* [CHANGED] Overhauled button style for fintech card-like appearance */
div[data-testid="stButton"] > button {{
    background: {THEME["surface2"]} !important;
    color: {THEME["text"]} !important;
    border: 1.4px solid {THEME["border"]} !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    width: 100% !important;
    text-align: left !important;
    transition: border-color 0.18s, background 0.18s !important;
    cursor: pointer !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 52px !important;
}}

div[data-testid="stButton"] > button:hover {{
    border-color: {THEME["green"]} !important;
    background: {THEME["green_soft"]} !important;
    color: {THEME["green"]} !important;
}}

/* Toggle button — circular, icon-only */
/* [CHANGED] Specific override for the toggle button rendered separately */
div[data-testid="stButton"].toggle-btn > button {{
    background: {THEME["toggle_bg"]} !important;
    border: 1.4px solid {THEME["border"]} !important;
    border-radius: 50% !important;
    width: 30px !important;
    min-width: 30px !important;
    max-width: 30px !important;
    min-height: 30px !important;
    height: 30px !important;
    max-height: 30px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.82rem !important;
    line-height: 1 !important;
}}

/* ── Text input ── */
/* [CHANGED] Styled input box with green focus ring */
div[data-testid="stTextInput"] input {{
    background: {THEME["surface"]} !important;
    color: {THEME["text"]} !important;
    border: 1.5px solid {THEME["border"]} !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.18s !important;
}}

div[data-testid="stTextInput"] input:focus {{
    border-color: {THEME["green"]} !important;
    box-shadow: 0 0 0 3px {THEME["green_soft"]} !important;
    outline: none !important;
}}

div[data-testid="stTextInput"] label {{
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: {THEME["subtext"]} !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}}

/* ── Answer block ── */
/* [CHANGED] Custom answer card replacing st.success() default green box */
.mf-answer-card {{
    background: {THEME["answer_bg"]};
    border: 1.5px solid {THEME["answer_border"]};
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 0.93rem;
    line-height: 1.65;
    color: {THEME["text"]};
    margin-top: 6px;
    white-space: pre-wrap;
    word-break: break-word;
}}

.mf-answer-label {{
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: {THEME["green"]};
    margin-bottom: 8px;
}}

/* ── Spinner colour ── */
div[data-testid="stSpinner"] svg circle {{
    stroke: {THEME["green"]} !important;
}}

/* ── Footer caption ── */
/* [CHANGED] Softer footer styling */
div[data-testid="stCaptionContainer"] p,
.mf-footer {{
    font-size: 0.73rem !important;
    color: {THEME["subtext"]} !important;
    text-align: center;
    margin-top: 8px;
}}

/* ── Error state ── */
.mf-error {{
    background: #2e0e0e;
    border: 1.5px solid #cc3333;
    border-radius: 10px;
    padding: 14px 18px;
    color: #ff6b6b;
    font-size: 0.88rem;
}}
</style>
""", unsafe_allow_html=True)

# ── BACKEND CONFIG (unchanged) ────────────────────────────────────────────────
API_URL = "https://rag-mf-chatbot-1.onrender.com/ask"

# ── HEADER: Groww logo + badge + dark-mode toggle ─────────────────────────────
# [CHANGED] Custom navbar rendered as HTML + a Streamlit button for the toggle
col_logo, col_right = st.columns([6, 1])

with col_logo:
    st.markdown(f"""
    <div class="mf-navbar">
        <div class="mf-logo">
            Groww<span>mutual funds</span>
        </div>
        <div class="mf-right">
            <span class="mf-badge">HDFC AMC · Facts Only</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    # Circular icon-only toggle button
    st.markdown('<div class="toggle-btn">', unsafe_allow_html=True)
    st.button(
        THEME["toggle_icon"],
        key="theme_toggle",
        on_click=toggle_theme,
        help="Switch between light and dark mode"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ── PAGE TITLE ────────────────────────────────────────────────────────────────
# [CHANGED] Replaced st.title() + st.markdown() with styled HTML
st.markdown(f"""
<div class="mf-title">📊 Mutual Fund FAQ Assistant</div>
<div class="mf-subtitle">Facts-only answers. No investment advice. Sources cited in every reply.</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="mf-divider">', unsafe_allow_html=True)

# ── EXAMPLE QUESTION BUTTONS ──────────────────────────────────────────────────
# [CHANGED] Section label + 2×2 grid (logic identical to original)
st.markdown('<div class="mf-section-label">🔍 Try a question</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if st.button("💹  Expense ratio of HDFC Top 100 Fund"):
        st.session_state.query = "What is expense ratio of HDFC Top 100 Fund?"

    if st.button("🔒  ELSS lock-in period"):
        st.session_state.query = "What is ELSS lock-in period?"

with col2:
    if st.button("📄  Download MF statement"):
        st.session_state.query = "How to download mutual fund statement?"

    if st.button("💰  Exit load of Balanced Advantage Fund"):
        st.session_state.query = "What is exit load of HDFC Balanced Advantage Fund?"

st.markdown('<hr class="mf-divider">', unsafe_allow_html=True)

# ── TEXT INPUT ────────────────────────────────────────────────────────────────
# [CHANGED] Label text improved; logic identical to original
query = st.text_input(
    "Your question",
    value=st.session_state.get("query", ""),
    placeholder="e.g. What is the riskometer of HDFC Flexi Cap Fund?",
)

# ── API CALL & ANSWER (logic unchanged) ──────────────────────────────────────
if query:
    with st.spinner("Fetching answer…"):
        try:
            response = requests.post(API_URL, json={"question": query})
            response.raise_for_status()
            answer = response.json()["answer"]
            # [CHANGED] Replaced st.success() with custom styled card
            st.markdown('<div class="mf-answer-label">💬 Answer</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mf-answer-card">{answer}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(
                f'<div class="mf-error">⚠️ Could not reach the server. Please try again.<br>'
                f'<small style="opacity:0.6">{str(e)}</small></div>',
                unsafe_allow_html=True,
            )

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="mf-divider">', unsafe_allow_html=True)
# [CHANGED] Footer copy slightly expanded for clarity
st.markdown(
    '<div class="mf-footer">'
    'Data sourced from HDFC AMC, AMFI, SEBI, and Groww. '
    'This tool provides factual information only and does not constitute investment advice.'
    '</div>',
    unsafe_allow_html=True,
)