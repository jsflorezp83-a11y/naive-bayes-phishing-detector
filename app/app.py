# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import streamlit as st
import joblib

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Detector de Phishing",
    page_icon="📧",
    layout="centered"
)

# ==========================================
# CARGAR MODELO Y VECTORIZADOR
# ==========================================

model = joblib.load('models/modelo.pkl')

vectorizer = joblib.load('models/vectorizer.pkl')

# ==========================================
# TÍTULO PRINCIPAL
# ==========================================

st.title("📧 Detector de Correos Phishing")

st.write("""
Esta aplicación utiliza Machine Learning y el algoritmo Naive Bayes
para detectar si un correo electrónico es phishing o legítimo.
""")

# ==========================================
# INPUT DEL USUARIO
# ==========================================

st.subheader("✍️ Ingrese el contenido del correo")

email_text = st.text_area(
    "Texto del correo electrónico",
    height=250
)

# ==========================================
# BOTÓN DE PREDICCIÓN
# ==========================================

if st.button("🔍 Analizar Correo"):

    # Verificar si el usuario escribió algo
    if email_text.strip() == "":

        st.warning("⚠️ Por favor ingrese un correo electrónico.")

    else:

        # ==========================================
        # PREPROCESAMIENTO
        # ==========================================

        email_vector = vectorizer.transform([email_text])

        # ==========================================
        # PREDICCIÓN
        # ==========================================

        prediction = model.predict(email_vector)

        probability = model.predict_proba(email_vector)

        # ==========================================
        # MOSTRAR RESULTADOS
        # ==========================================

        st.subheader("📊 Resultado del análisis")

        # Si es phishing
        if prediction[0] == 1:

            st.error("⚠️ Este correo es PHISHING")

            st.write(
                f"Probabilidad de phishing: "
                f"{probability[0][1] * 100:.2f}%"
            )

        # Si es legítimo
        else:

            st.success("✅ Este correo es LEGÍTIMO")

            st.write(
                f"Probabilidad de ser legítimo: "
                f"{probability[0][0] * 100:.2f}%"
            )

# ==========================================
# PIE DE PÁGINA
# ==========================================

st.markdown("---")

st.caption(
    "Proyecto de Machine Learning - "
    "Detección de Correos Phishing con Naive Bayes"
)