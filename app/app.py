import streamlit as st
import joblib
import re
import time
import plotly.express as px

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="PhishGuard",
    layout="centered"
)

# ==========================================
# ESTILOS
# ==========================================

st.markdown("""
<style>

.stApp{
    background-color:#000000;
    color:white;
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
    box-shadow:0 0 15px rgba(0,212,255,0.25);
    margin-bottom:20px;
}

h1,h2,h3,p,label{
    color:white !important;
}

.stButton > button{
    background:linear-gradient(90deg,#00d4ff,#0078ff);
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    width:250px;
    font-size:18px;
    font-weight:bold;
    transition:0.3s;
}

.stButton > button:hover{
    transform:scale(1.05);
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

</style>
""", unsafe_allow_html=True)

# ==========================================
# CONTROL DE PÁGINAS
# ==========================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# ==========================================
# PÁGINA DE INICIO
# ==========================================

if st.session_state.pagina == "inicio":

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<p class="main-title">PhishGuard</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="card">

    <h3>Sistema Inteligente de Detección de Phishing</h3>

    Esta herramienta utiliza Machine Learning para
    analizar correos electrónicos y detectar posibles
    intentos de fraude, robo de credenciales y ataques
    de ingeniería social.

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Iniciar Analisis"):
        st.session_state.pagina = "detector"
        st.rerun()

# ==========================================
# DETECTOR
# ==========================================

elif st.session_state.pagina == "detector":

    model = joblib.load("models/modelo.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")

    st.markdown(
        '<p class="main-title">Analizador de Correos</p>',
        unsafe_allow_html=True
    )

    st.write(
        "Ingrese el contenido del correo electrónico para realizar el análisis."
    )

    email_text = st.text_area(
        "Contenido del correo",
        height=250
    )

    if st.button("Analizar Correo"):

        if email_text.strip() == "":

            st.warning(
                "Por favor ingrese un correo electrónico."
            )

        else:

            with st.spinner("Analizando correo..."):
                time.sleep(2)

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
                # VECTORIZACIÓN
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
                # REGLA HEURÍSTICA
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
                # RIESGO
                # ==========================================

                if prediction[0] == 1:
                    riesgo = probability[0][1]
                else:
                    riesgo = 1 - probability[0][0]

                st.subheader("Resultado del Análisis")

                # ==========================================
                # RESULTADO
                # ==========================================

                if prediction[0] == 1:

                    st.error(
                        "Este correo fue clasificado como PHISHING"
                    )

                    st.write(
                        f"Probabilidad de phishing: "
                        f"{probability[0][1]*100:.2f}%"
                    )

                else:

                    st.success(
                        "Este correo fue clasificado como LEGÍTIMO"
                    )

                    st.write(
                        f"Probabilidad de legitimidad: "
                        f"{probability[0][0]*100:.2f}%"
                    )

                # ==========================================
                # BARRA DE RIESGO
                # ==========================================

                st.write("Nivel de Riesgo")

                st.progress(
                    float(riesgo)
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

                    st.metric(
                        "Nivel de Riesgo",
                        f"{riesgo*100:.1f}%"
                    )

                # ==========================================
                # GRÁFICO
                # ==========================================

                if prediction[0] == 1:

                    datos = {
                        "Categoria": [
                            "Phishing",
                            "Legitimo"
                        ],
                        "Valor": [
                            probability[0][1]*100,
                            (1-probability[0][1])*100
                        ]
                    }

                else:

                    datos = {
                        "Categoria": [
                            "Legitimo",
                            "Phishing"
                        ],
                        "Valor": [
                            probability[0][0]*100,
                            (1-probability[0][0])*100
                        ]
                    }

                fig = px.pie(
                    values=datos["Valor"],
                    names=datos["Categoria"],
                    title="Distribucion de Probabilidades",
                    hole=0.45
                )

                fig.update_layout(
                    paper_bgcolor="black",
                    plot_bgcolor="black",
                    font_color="white"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Volver al Inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Proyecto de Machine Learning - Detección de Correos Phishing"
)