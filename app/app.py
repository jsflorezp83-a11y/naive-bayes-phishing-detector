# app.py

import streamlit as st
import joblib
import re

# ==========================================

# CONFIGURACIÓN DE LA PÁGINA

# ==========================================

st.set_page_config(
page_title="PhishGuard",
layout="centered"
)

# ==========================================

# ESTILOS PERSONALIZADOS

# ==========================================

st.markdown("""

<style>

.stApp{
    background: linear-gradient(
        135deg,
        #050505,
        #0d1b2a,
        #000000
    );
}

.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    color:#00d4ff;
    text-shadow:0px 0px 15px #00d4ff;
}

.card{
    background:#111111;
    padding:25px;
    border-radius:15px;
    border:1px solid #00d4ff;
    box-shadow:0px 0px 15px rgba(0,212,255,0.20);
    margin-bottom:20px;
}

.stButton > button{
    background:linear-gradient(
        90deg,
        #00d4ff,
        #0078ff
    );
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
    font-weight:bold;
}

.stButton > button:hover{
    transform:scale(1.02);
}

.stTextArea textarea{
    background-color:#151515;
    color:white;
    border:1px solid #00d4ff;
    border-radius:10px;
}

[data-testid="stMetric"]{
    background:#111111;
    border:1px solid #00d4ff;
    border-radius:12px;
    padding:15px;
}

h1,h2,h3,p,label{
    color:white !important;
}

</style>

""", unsafe_allow_html=True)

# ==========================================

# SIDEBAR

# ==========================================

with st.sidebar:


st.title("PhishGuard")

st.info("""
Sistema Inteligente de Detección
de Correos Phishing.
""")

st.divider()

st.subheader("Tecnologías")

st.write("Python")
st.write("Streamlit")
st.write("Scikit-Learn")
st.write("Naive Bayes")


# ==========================================

# CARGAR MODELO

# ==========================================

model = joblib.load(
'models/modelo.pkl'
)

vectorizer = joblib.load(
'models/vectorizer.pkl'
)

# ==========================================

# ENCABEZADO

# ==========================================

st.markdown(
'<p class="main-title">PhishGuard</p>',
unsafe_allow_html=True
)

st.markdown("""

<div class="card">

<h3>Sistema Inteligente de Detección de Phishing</h3>

Esta herramienta utiliza Machine Learning
para analizar correos electrónicos y detectar
posibles intentos de fraude, robo de credenciales
y ataques de ingeniería social.

</div>
""", unsafe_allow_html=True)

# ==========================================

# MÉTRICAS INICIALES

# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
st.metric(
"Modelo",
"Naive Bayes"
)

with col2:
st.metric(
"Estado",
"Activo"
)

with col3:
st.metric(
"Análisis",
"Tiempo Real"
)

# ==========================================

# INPUT

# ==========================================

st.subheader(
"Ingrese el contenido del correo"
)

email_text = st.text_area(
"Texto del correo electrónico",
height=250
)

# ==========================================

# BOTÓN

# ==========================================

if st.button("Analizar Correo"):


if email_text.strip() == "":

    st.warning(
        "Por favor ingrese un correo electrónico."
    )

else:

    original_text = email_text

    # ==========================================
    # PREPROCESAMIENTO
    # ==========================================

    email_text = email_text.lower()

    email_text = re.sub(
        r'http\\S+',
        '',
        email_text
    )

    email_text = re.sub(
        r'[^a-zA-Z\\s]',
        '',
        email_text
    )

    # ==========================================
    # TRANSFORMACIÓN
    # ==========================================

    email_vector = vectorizer.transform(
        [email_text]
    )

    # ==========================================
    # PREDICCIÓN
    # ==========================================

    prediction = model.predict(
        email_vector
    )

    probability = model.predict_proba(
        email_vector
    )

    # ==========================================
    # PALABRAS SOSPECHOSAS
    # ==========================================

    suspicious_words = [

        'verify',
        'password',
        'bank',
        'account',
        'suspended',
        'urgent',
        'click',
        'login',
        'security',
        'confirm',
        'limited',
        'identity',
        'alert',
        'access',
        'update',
        'warning',
        'locked',
        'expire',
        'reset',
        'credential'

    ]

    suspicious_count = sum(
        word in email_text
        for word in suspicious_words
    )

    # ==========================================
    # HEURÍSTICA
    # ==========================================

    if suspicious_count >= 3:

        prediction[0] = 1

        probability[0][1] += (
            suspicious_count * 0.03
        )

        probability[0][1] = min(
            probability[0][1],
            0.99
        )

    # ==========================================
    # RESULTADO
    # ==========================================

    st.subheader(
        "Resultado del análisis"
    )

    if prediction[0] == 1:

        st.error(
            "Este correo es PHISHING"
        )

        st.write(
            f"Probabilidad de phishing: "
            f"{probability[0][1] * 100:.2f}%"
        )

    else:

        st.success(
            "Este correo es LEGÍTIMO"
        )

        st.write(
            f"Probabilidad de legitimidad: "
            f"{probability[0][0] * 100:.2f}%"
        )

    # ==========================================
    # RIESGO
    # ==========================================

    if prediction[0] == 1:

        riesgo = probability[0][1]

    else:

        riesgo = (
            1 - probability[0][0]
        )

    st.subheader(
        "Nivel de Riesgo"
    )

    st.progress(
        float(riesgo)
    )

    st.write(
        f"Riesgo estimado: "
        f"{riesgo*100:.2f}%"
    )

    # ==========================================
    # MÉTRICAS
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Palabras Sospechosas",
            suspicious_count
        )

    with col2:

        confianza = (
            max(probability[0]) * 100
        )

        st.metric(
            "Confianza del Modelo",
            f"{confianza:.2f}%"
        )


# ==========================================

# FOOTER

# ==========================================

st.markdown("---")

st.caption(
"Proyecto de Machine Learning - "
"Detección de Correos Phishing"
)
