import streamlit as st
import joblib
import re
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="PhishGuard | Detector de Phishing",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# ESTILOS GLOBALES
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background: #050a0e;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 800px; }

h1, h2, h3 { font-family: 'Space Mono', monospace !important; color: #ffffff !important; }

.pg-logo { text-align: center; margin-bottom: 0.25rem; }
.pg-logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 3.2rem;
    font-weight: 700;
    color: #00d4ff;
    letter-spacing: -1px;
    text-shadow: 0 0 30px rgba(0,212,255,0.4), 0 0 60px rgba(0,212,255,0.15);
}
.pg-logo-badge {
    display: inline-block;
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #64748b;
    border: 1px solid #1e293b;
    border-radius: 20px;
    padding: 3px 12px;
    margin-top: 4px;
}
.pg-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #64748b;
    text-align: center;
    margin-top: 0.75rem;
    margin-bottom: 2rem;
}

.pg-card {
    background: linear-gradient(135deg, #0d1520 0%, #0a1018 100%);
    border: 1px solid #1a2a3a;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.pg-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    opacity: 0.5;
}
.pg-card-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #00d4ff;
    margin-bottom: 1rem;
}

.pg-features {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin: 1.5rem 0;
}
.pg-feature-tag {
    background: #0d1a26;
    border: 1px solid #1a3040;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.8rem;
    color: #7dd3fc;
    display: flex;
    align-items: center;
    gap: 6px;
}
.pg-feature-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00d4ff;
    flex-shrink: 0;
}

.stButton {
    padding: 0 !important;
    margin: 0 !important;
}
.stButton > button, .stButton > button > div, .stButton > button p {
    background: linear-gradient(135deg, #0078ff 0%, #00b4d8 100%) !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 10px !important;
    height: 52px !important;
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.3s ease !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 !important;
    border-color: transparent !important;
}
.stButton > button:hover, .stButton > button:hover > div, .stButton > button:hover p {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,120,255,0.5) !important;
    color: #000000 !important;
    outline: none !important;
    border: none !important;
}
.stButton > button:focus, .stButton > button:focus-visible, .stButton > button:active {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
    border-color: transparent !important;
}
.stButton > button[data-baseweb="button"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}
div[data-testid="stBaseButton-secondary"] {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

.stTextArea textarea {
    background: #060d14 !important;
    color: #cbd5e1 !important;
    border: 1px solid #1a2a3a !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
    caret-color: #00d4ff !important;
}
.stTextArea textarea:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}
.stTextArea label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #00d4ff !important;
}

[data-testid="stMetric"] {
    background: #0a1018 !important;
    border: 1px solid #1a2a3a !important;
    border-radius: 12px !important;
    padding: 1.2rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.8rem !important;
    color: #e2e8f0 !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #00b4d8, #ff4757) !important;
    border-radius: 4px !important;
}
.stProgress > div > div {
    background: #1a2a3a !important;
    border-radius: 4px !important;
    height: 10px !important;
}

.pg-result-phishing {
    background: linear-gradient(135deg, #1a0808 0%, #120505 100%);
    border: 1px solid #7f1d1d;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.pg-result-phishing::before {
    content: '⚠ PHISHING DETECTADO';
    display: block;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #ef4444;
    margin-bottom: 0.5rem;
}
.pg-result-legit {
    background: linear-gradient(135deg, #061a0e 0%, #041209 100%);
    border: 1px solid #14532d;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.pg-result-legit::before {
    content: '✓ CORREO LEGÍTIMO';
    display: block;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #22c55e;
    margin-bottom: 0.5rem;
}
.pg-result-value {
    font-family: 'Space Mono', monospace;
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}
.pg-result-phishing .pg-result-value { color: #ef4444; }
.pg-result-legit .pg-result-value { color: #22c55e; }
.pg-result-label { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }

.pg-word-found {
    display: inline-block;
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 6px;
    padding: 3px 10px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #fca5a5;
    margin: 3px;
}

.pg-history-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #0a1018;
    border: 1px solid #1a2a3a;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
}
.pg-history-dot-phishing { width:10px; height:10px; border-radius:50%; background:#ef4444; flex-shrink:0; }
.pg-history-dot-legit    { width:10px; height:10px; border-radius:50%; background:#22c55e; flex-shrink:0; }

.pg-divider { border: none; border-top: 1px solid #1a2a3a; margin: 2rem 0; }

.stTabs [data-baseweb="tab-list"] {
    background: #0a1018 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #64748b !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: #162030 !important;
    color: #00d4ff !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

.pg-footer {
    text-align: center;
    font-size: 0.75rem;
    color: #2d3f52;
    margin-top: 3rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
}

details { background: #0a1018 !important; border: 1px solid #1a2a3a !important; border-radius: 10px !important; }
summary { font-family: 'Space Mono', monospace !important; font-size: 0.75rem !important; color: #94a3b8 !important; letter-spacing: 0.08em !important; }

p, li, span, div { color: #94a3b8; }
label { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# ESTADO DE LA SESIÓN
# ==========================================

def init_state():
    defaults = {
        "pagina": "inicio",
        "historial": [],
        "total_analizados": 0,
        "total_phishing": 0,
        "total_legitimos": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ==========================================
# PALABRAS SOSPECHOSAS
# ==========================================

SUSPICIOUS_WORDS = [
    'verify', 'password', 'bank', 'account', 'suspended', 'urgent',
    'click', 'login', 'security', 'confirm', 'limited', 'identity',
    'alert', 'access', 'update', 'warning', 'locked', 'expire',
    'reset', 'credential', 'unauthorized', 'validate', 'immediately',
    'action required', 'winner', 'prize', 'free', 'offer', 'congratulations',
    'unusual activity', 'verify now', 'sign in', 'billing', 'payment',
    'invoice', 'refund', 'customer support', 'dear user', 'dear customer'
]


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def preprocess_email(text: str) -> str:
    text = text.lower()
    text = re.sub(r'http\S+|www\.\S+', '', text)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def find_suspicious_words(text: str) -> list:
    return [w for w in SUSPICIOUS_WORDS if w in text.lower()]

def calculate_risk_level(riesgo_pct: float) -> tuple:
    if riesgo_pct < 25:   return "MUY BAJO", "#22c55e"
    elif riesgo_pct < 50: return "BAJO",     "#84cc16"
    elif riesgo_pct < 70: return "MODERADO", "#f59e0b"
    elif riesgo_pct < 85: return "ALTO",     "#f97316"
    else:                 return "CRÍTICO",  "#ef4444"

def word_count(text: str) -> int:
    return len(text.split())

def url_count(text: str) -> int:
    return len(re.findall(r'http\S+|www\.\S+', text))

def uppercase_ratio(text: str) -> float:
    letters = [c for c in text if c.isalpha()]
    if not letters: return 0.0
    return sum(1 for c in letters if c.isupper()) / len(letters)


# ==========================================
# CARGA DEL MODELO
# ==========================================

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        model      = joblib.load("models/modelo.pkl")
        vectorizer = joblib.load("models/vectorizer.pkl")
        return model, vectorizer
    except Exception:
        return None, None


# ==========================================
# PÁGINA: INICIO
# ==========================================

def page_inicio():
    st.markdown('<div class="pg-logo"><span class="pg-logo-text">PhishGuard</span></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center"><span class="pg-logo-badge">v2.0 · ML-Powered</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="pg-subtitle">Sistema inteligente de detección de phishing y amenazas por correo electrónico</p>', unsafe_allow_html=True)

    if st.session_state.total_analizados > 0:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Analizados", st.session_state.total_analizados)
        with c2: st.metric("Phishing",   st.session_state.total_phishing)
        with c3: st.metric("Legítimos",  st.session_state.total_legitimos)
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)

    st.markdown("""
    <div class="pg-card">
        <div class="pg-card-title">¿Qué es PhishGuard?</div>
        <p style="color:#94a3b8; line-height:1.8; font-size:0.9rem;">
            PhishGuard combina un modelo de Machine Learning entrenado con miles de correos reales
            con análisis heurístico de patrones linguísticos para detectar intentos de fraude,
            robo de credenciales y ataques de ingeniería social con alta precisión.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pg-features">
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Análisis con ML</div>
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Detección Heurística</div>
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Análisis de URLs</div>
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Palabras Clave</div>
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Nivel de Riesgo</div>
        <div class="pg-feature-tag"><span class="pg-feature-dot"></span>Historial Local</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("  Iniciar Análisis", use_container_width=True):
            st.session_state.pagina = "detector"
            st.rerun()

    if st.session_state.historial:
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="pg-card-title">Análisis Recientes</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.historial[-5:]):
            dot_class   = "pg-history-dot-phishing" if item["tipo"] == "PHISHING" else "pg-history-dot-legit"
            st.markdown(f"""
            <div class="pg-history-item">
                <div class="{dot_class}"></div>
                <div class="pg-history-text" style="font-size:0.8rem;color:#94a3b8;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{item['preview']}</div>
                <div class="pg-history-time" style="font-family:'Space Mono',monospace;font-size:0.65rem;color:#475569;flex-shrink:0;">{item['hora']} · {item['riesgo']:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# PÁGINA: DETECTOR
# ==========================================

def page_detector():
    st.markdown('<div class="pg-logo"><span class="pg-logo-text" style="font-size:2rem;">PhishGuard</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="pg-subtitle" style="margin-bottom:1.5rem;">Analizador de Correos Electrónicos</p>', unsafe_allow_html=True)

    tab_analizar, tab_info, tab_historial = st.tabs(["  Analizar", "  Indicadores", "  Historial"])

    with tab_analizar:   _tab_analizar()
    with tab_info:       _tab_indicadores()
    with tab_historial:  _tab_historial()

    st.markdown("<br>", unsafe_allow_html=True)
    col_back = st.columns([1, 2, 1])
    with col_back[1]:
        if st.button("← Volver al Inicio", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()


def _tab_analizar():
    model, vectorizer = load_model()

    if model is None:
        st.error("⚠ No se encontró el modelo en `models/modelo.pkl`. Verifica que los archivos existan.")
        return

    email_text = st.text_area(
        "Contenido del correo electrónico",
        height=220,
        placeholder="Pega aquí el contenido completo del correo que deseas analizar...",
        key="email_input"
    )

    if email_text.strip():
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Palabras",    word_count(email_text))
        with c2: st.metric("URLs",        url_count(email_text))
        with c3: st.metric("Mayúsculas",  f"{uppercase_ratio(email_text)*100:.0f}%")
        with c4: st.metric("Caracteres",  len(email_text))

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        analizar = st.button("  Analizar Correo", use_container_width=True)

    if analizar:
        if not email_text.strip():
            st.warning("Por favor ingresa el contenido del correo antes de analizar.")
            return

        with st.spinner("Procesando con modelo de ML..."):
            time.sleep(1.5)

            email_clean     = preprocess_email(email_text)
            found_words     = find_suspicious_words(email_text)
            suspicious_count = len(found_words)
            email_vector    = vectorizer.transform([email_clean])
            prediction      = model.predict(email_vector)
            probability     = model.predict_proba(email_vector)

            prob_phishing = float(probability[0][1])
            prob_legit    = float(probability[0][0])

            if suspicious_count >= 3:
                prediction[0] = 1
                prob_phishing = min(prob_phishing + suspicious_count * 0.03, 0.99)
                prob_legit    = 1 - prob_phishing

            if url_count(email_text) >= 3:
                prob_phishing = min(prob_phishing + 0.05, 0.99)
                prob_legit    = 1 - prob_phishing

            if uppercase_ratio(email_text) > 0.35:
                prob_phishing = min(prob_phishing + 0.04, 0.99)
                prob_legit    = 1 - prob_phishing

            is_phishing = (prediction[0] == 1)
            riesgo      = prob_phishing if is_phishing else (1 - prob_legit)
            riesgo_pct  = riesgo * 100
            risk_label, risk_color = calculate_risk_level(riesgo_pct)

            preview = email_text[:60].replace("\n", " ") + ("..." if len(email_text) > 60 else "")
            st.session_state.historial.append({
                "tipo":     "PHISHING" if is_phishing else "LEGÍTIMO",
                "riesgo":   riesgo_pct,
                "preview":  preview,
                "hora":     datetime.now().strftime("%H:%M"),
                "palabras": suspicious_count,
                "urls":     url_count(email_text),
            })
            st.session_state.total_analizados += 1
            if is_phishing: st.session_state.total_phishing  += 1
            else:           st.session_state.total_legitimos += 1

        # ---- Resultado principal ----
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)

        if is_phishing:
            st.markdown(f"""
            <div class="pg-result-phishing">
                <div class="pg-result-value">{riesgo_pct:.1f}%</div>
                <div class="pg-result-label">Probabilidad de ser Phishing · Nivel: <strong style="color:{risk_color}">{risk_label}</strong></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="pg-result-legit">
                <div class="pg-result-value">{prob_legit*100:.1f}%</div>
                <div class="pg-result-label">Probabilidad de ser Legítimo · Riesgo: <strong style="color:{risk_color}">{risk_label}</strong></div>
            </div>
            """, unsafe_allow_html=True)

        # ---- Barra de riesgo ----
        st.markdown('<div class="pg-card-title" style="margin-top:1.5rem;">Nivel de Riesgo</div>', unsafe_allow_html=True)
        st.progress(float(min(riesgo, 1.0)))

        # ---- Métricas ----
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Riesgo",               f"{riesgo_pct:.1f}%")
        with c2: st.metric("Palabras Sospechosas",  suspicious_count)
        with c3: st.metric("URLs detectadas",        url_count(email_text))
        with c4: st.metric("Mayúsculas",             f"{uppercase_ratio(email_text)*100:.0f}%")

        # ---- Palabras encontradas ----
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="pg-card-title">Palabras Sospechosas Detectadas</div>', unsafe_allow_html=True)
        if found_words:
            tags_html = "".join([f'<span class="pg-word-found">{w}</span>' for w in found_words])
            st.markdown(f'<div style="margin-top:0.5rem;">{tags_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#475569; font-size:0.85rem;">No se encontraron palabras sospechosas.</p>', unsafe_allow_html=True)

        # ---- Gráficos ----
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="pg-card-title">Distribución de Probabilidades</div>', unsafe_allow_html=True)

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=riesgo_pct,
                number={"suffix": "%", "font": {"size": 28, "color": "#e2e8f0", "family": "Space Mono"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#1a2a3a", "tickwidth": 1},
                    "bar": {"color": risk_color, "thickness": 0.25},
                    "bgcolor": "#0a1018",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0,  25],  "color": "#061a0e"},
                        {"range": [25, 50],  "color": "#0e1a08"},
                        {"range": [50, 70],  "color": "#1a1400"},
                        {"range": [70, 85],  "color": "#1a0a00"},
                        {"range": [85, 100], "color": "#1a0000"},
                    ],
                    "threshold": {"line": {"color": risk_color, "width": 4}, "thickness": 0.75, "value": riesgo_pct}
                },
                title={"text": "Nivel de Riesgo", "font": {"color": "#64748b", "size": 12, "family": "Space Mono"}}
            ))
            fig_gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=220,
                margin=dict(t=40, b=10, l=20, r=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_g2:
            fig_pie = px.pie(
                values=[prob_phishing * 100, prob_legit * 100],
                names=["Phishing", "Legítimo"],
                hole=0.55,
                color_discrete_sequence=["#ef4444", "#22c55e"]
            )
            fig_pie.update_traces(
                textfont=dict(family="Space Mono", color="#e2e8f0"),
                marker=dict(line=dict(color="#050a0e", width=2))
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8", family="Inter"),
                legend=dict(font=dict(color="#94a3b8", size=11), bgcolor="rgba(0,0,0,0)"),
                height=220,
                margin=dict(t=20, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        # ---- Recomendaciones ----
        st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="pg-card-title">Recomendaciones</div>', unsafe_allow_html=True)

        if is_phishing and riesgo_pct >= 70:
            st.markdown("""
            <div class="pg-card" style="border-color:#7f1d1d;">
            <p style="color:#fca5a5; font-size:0.9rem; line-height:1.8;">
             <strong style="color:#f87171;">No hagas clic</strong> en ningún enlace ni descargues adjuntos.<br>
             <strong style="color:#f87171;">Elimina</strong> este correo de inmediato.<br>
             <strong style="color:#f87171;">No compartas</strong> contraseñas ni datos bancarios.<br>
             <strong style="color:#f87171;">Reporta</strong> el correo como phishing a tu proveedor.<br>
             Si ya interactuaste, <strong style="color:#f87171;">cambia tus contraseñas</strong> de inmediato.
            </p>
            </div>
            """, unsafe_allow_html=True)
        elif is_phishing:
            st.markdown("""
            <div class="pg-card" style="border-color:#92400e;">
            <p style="color:#fcd34d; font-size:0.9rem; line-height:1.8;">
             - Este correo presenta indicadores sospechosos. Procede con cautela.<br>
             - Verifica la dirección del remitente y el dominio.<br>
             - No hagas clic en enlaces sin verificar su destino.
            </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="pg-card" style="border-color:#14532d;">
            <p style="color:#86efac; font-size:0.9rem; line-height:1.8;">
             - Este correo parece legítimo. Sin embargo, mantén buenas prácticas:<br>
             - Verifica siempre el remitente antes de responder.<br>
             - No hagas clic en enlaces inesperados aunque el correo parezca confiable.
            </p>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Ver texto procesado por el modelo"):
            st.code(email_clean, language=None)


def _tab_indicadores():
    st.markdown('<div class="pg-card-title">¿Qué analiza PhishGuard?</div>', unsafe_allow_html=True)

    indicadores = [
        ("Modelo de ML",        f"Clasificador entrenado con miles de correos reales usando TF-IDF + Naive Bayes / Random Forest."),
        ("Palabras Clave",       f"Se verifican {len(SUSPICIOUS_WORDS)} palabras frecuentes en correos de phishing."),
        ("Detección de URLs",    "Más de 3 URLs en un correo incrementa la puntuación de riesgo automáticamente."),
        ("Exceso de Mayúsculas", "Un ratio mayor al 35% de mayúsculas es señal de alerta heurística."),
        ("Score Combinado",      "El resultado combina la probabilidad del modelo con penalizaciones heurísticas."),
    ]

    for titulo, desc in indicadores:
        st.markdown(f"""
        <div class="pg-card" style="padding:1.2rem 1.5rem; margin-bottom:10px;">
            <div style="display:flex; gap:1rem; align-items:flex-start;">
                <div style="font-size:1.4rem; flex-shrink:0;"
                <div>
                    <div style="font-family:'Space Mono',monospace; font-size:0.75rem; color:#00d4ff; margin-bottom:4px; letter-spacing:0.08em;">{titulo.upper()}</div>
                    <div style="font-size:0.85rem; color:#94a3b8; line-height:1.7;">{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="pg-card-title">Escala de Riesgo</div>', unsafe_allow_html=True)

    niveles = [
        ("0% – 24%",   "MUY BAJO", "#22c55e", "Casi con certeza es legítimo."),
        ("25% – 49%",  "BAJO",     "#84cc16", "Bajo riesgo, verificar si hay dudas."),
        ("50% – 69%",  "MODERADO", "#f59e0b", "Precaución recomendada."),
        ("70% – 84%",  "ALTO",     "#f97316", "Probablemente es phishing."),
        ("85% – 100%", "CRÍTICO",  "#ef4444", "Phishing confirmado. No interactúes."),
    ]

    for rango, etiqueta, color, desc in niveles:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:1rem; padding:10px 0; border-bottom: 1px solid #1a2a3a;">
            <div style="width:90px; font-family:'Space Mono',monospace; font-size:0.7rem; color:#475569; flex-shrink:0;">{rango}</div>
            <div style="width:80px; font-family:'Space Mono',monospace; font-size:0.7rem; font-weight:700; color:{color}; flex-shrink:0;">{etiqueta}</div>
            <div style="font-size:0.82rem; color:#94a3b8;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)


def _tab_historial():
    if not st.session_state.historial:
        st.markdown('<p style="color:#475569; font-size:0.9rem; text-align:center; margin-top:2rem;">No hay análisis previos en esta sesión.</p>', unsafe_allow_html=True)
        return

    total        = len(st.session_state.historial)
    phishing_n   = sum(1 for h in st.session_state.historial if h["tipo"] == "PHISHING")
    legit_n      = total - phishing_n
    avg_risk     = sum(h["riesgo"] for h in st.session_state.historial) / total

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total",           total)
    with c2: st.metric("Phishing",        phishing_n)
    with c3: st.metric("Legítimos",       legit_n)
    with c4: st.metric("Riesgo Promedio", f"{avg_risk:.0f}%")

    st.markdown("<hr class='pg-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="pg-card-title">Registros</div>', unsafe_allow_html=True)

    for item in reversed(st.session_state.historial):
        dot_class   = "pg-history-dot-phishing" if item["tipo"] == "PHISHING" else "pg-history-dot-legit"
        label_color = "#ef4444" if item["tipo"] == "PHISHING" else "#22c55e"
        st.markdown(f"""
        <div class="pg-history-item">
            <div class="{dot_class}"></div>
            <div style="flex:1; min-width:0;">
                <div style="font-size:0.8rem; color:#94a3b8; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{item['preview']}</div>
                <div style="font-size:0.7rem; color:#475569; margin-top:2px;">Palabras sospechosas: {item['palabras']} · URLs: {item['urls']}</div>
            </div>
            <div style="text-align:right; flex-shrink:0;">
                <div style="font-family:'Space Mono',monospace; font-size:0.7rem; color:{label_color}; font-weight:700;">{item['tipo']}</div>
                <div style="font-family:'Space Mono',monospace; font-size:0.65rem; color:#475569;">{item['hora']} · {item['riesgo']:.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_clear = st.columns([2, 1, 2])
    with col_clear[1]:
        if st.button("  Limpiar Historial", use_container_width=True):
            st.session_state.historial         = []
            st.session_state.total_analizados  = 0
            st.session_state.total_phishing    = 0
            st.session_state.total_legitimos   = 0
            st.rerun()


# ==========================================
# ROUTER PRINCIPAL
# ==========================================

if st.session_state.pagina == "inicio":
    page_inicio()
elif st.session_state.pagina == "detector":
    page_detector()

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="pg-footer">
    PhishGuard v2.0 · Machine Learning · Detección de Phishing<br>
    <span style="font-size:0.65rem; color:#1e2d3d;">Los resultados son orientativos y no reemplazan el juicio humano.</span>
</div>
""", unsafe_allow_html=True)
