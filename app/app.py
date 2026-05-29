import streamlit as st
import joblib
import re

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Detector de Phishing",
    page_icon="",
    layout="centered"
)

# ==========================================
# ESTILO NEGRO
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #000000;
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton > button {
    background-color: #00c853;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 250px;
    font-size: 18px;
    font-weight: bold;
}

.stTextArea textarea {
    background-color: #1e1e1e;
    color: white;
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

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.title("Detector Inteligente de Phishing")

    st.markdown("""
    ### Sistema de detección de correos fraudulentos

    Esta herramienta utiliza Machine Learning para
    identificar intentos de phishing y proteger
    a los usuarios contra posibles amenazas.
    """)

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3064/3064197.png",
        width=200
    )

    if st.button("Iniciar Análisis"):
        st.session_state.pagina = "detector"
        st.rerun()

# ==========================================
# PÁGINA DEL DETECTOR
# ==========================================

elif st.session_state.pagina == "detector":

    # Cargar modelo
    model = joblib.load('models/modelo.pkl')
    vectorizer = joblib.load('models/vectorizer.pkl')

    st.title("Detector de Correos Phishing")

    st.write("""
    Ingrese el contenido del correo electrónico
    para analizar si es legítimo o phishing.
    """)

    email_text = st.text_area(
        "Texto del correo electrónico",
        height=250
    )

    if st.button("Analizar Correo"):

        if email_text.strip() == "":
            st.warning(
                "Por favor ingrese un correo electrónico."
            )

        else:

            email_text = email_text.lower()

            email_text = re.sub(
                r'http\S+',
                '',
                email_text
            )

            email_text = re.sub(
                r'[^a-zA-Z\s]',
                '',
                email_text
            )

            email_vector = vectorizer.transform(
                [email_text]
            )

            prediction = model.predict(
                email_vector
            )

            probability = model.predict_proba(
                email_vector
            )

            suspicious_words = [
                'verify', 'password', 'bank',
                'account', 'suspended', 'urgent',
                'click', 'login', 'security',
                'confirm', 'limited', 'identity',
                'alert', 'access', 'update',
                'warning', 'locked', 'expire',
                'reset', 'credential'
            ]

            suspicious_count = sum(
                word in email_text
                for word in suspicious_words
            )

            if suspicious_count >= 3:
                prediction[0] = 1
                probability[0][1] += suspicious_count * 0.03
                probability[0][1] = min(
                    probability[0][1],
                    0.99
                )

            st.subheader("Resultado")

            if prediction[0] == 1:

                st.error(
                    "Este correo es PHISHING"
                )

                st.write(
                    f"Probabilidad de phishing: "
                    f"{probability[0][1] * 100:.2f}%"
                )

                st.write(
                    f"Palabras sospechosas detectadas: "
                    f"{suspicious_count}"
                )

            else:

                st.success(
                    "Este correo es LEGÍTIMO"
                )

                st.write(
                    f"Probabilidad de ser legítimo: "
                    f"{probability[0][0] * 100:.2f}%"
                )

    if st.button("Volver al Inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

st.markdown("---")
st.caption("Proyecto de Machine Learning - Detección de Correos Phishing")