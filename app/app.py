# ==========================================
# IMPORTAR LIBRERÍAS
# ==========================================

import streamlit as st

import joblib

import re

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

Esta aplicación utiliza Machine Learning
para detectar si un correo electrónico
es phishing o legítimo.

""")

# ==========================================
# INPUT DEL USUARIO
# ==========================================

st.subheader("Ingrese el contenido del correo")

email_text = st.text_area(

    "Texto del correo electrónico",

    height=250

)

# ==========================================
# BOTÓN DE ANÁLISIS
# ==========================================

if st.button("Analizar Correo"):

    # ==========================================
    # VALIDAR INPUT
    # ==========================================

    if email_text.strip() == "":

        st.warning(

            "Por favor ingrese un correo electrónico."

        )

    else:

        # ==========================================
        # PREPROCESAMIENTO
        # ==========================================

        # Convertir texto a minúsculas
        email_text = email_text.lower()

        # Eliminar enlaces
        email_text = re.sub(

            r'http\S+',

            '',

            email_text

        )

        # Eliminar caracteres especiales
        email_text = re.sub(

            r'[^a-zA-Z\s]',

            '',

            email_text

        )

        # ==========================================
        # TRANSFORMAR TEXTO
        # ==========================================

        email_vector = vectorizer.transform(

            [email_text]

        )

        # ==========================================
        # REALIZAR PREDICCIÓN
        # ==========================================

        prediction = model.predict(

            email_vector

        )

        # ==========================================
        # OBTENER PROBABILIDADES
        # ==========================================

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

        # ==========================================
        # CONTAR PALABRAS SOSPECHOSAS
        # ==========================================

        suspicious_count = sum(

            word in email_text

            for word in suspicious_words

        )

        # ==========================================
        # DETECCIÓN HEURÍSTICA
        # ==========================================

        if suspicious_count >= 3:

            prediction[0] = 1

            # Incrementar probabilidad gradualmente
            probability[0][1] += suspicious_count * 0.03

            # Limitar máximo a 99%
            probability[0][1] = min(

                probability[0][1],

                0.99

            )

        # ==========================================
        # MOSTRAR RESULTADO
        # ==========================================

        st.subheader("Resultado del análisis")

        # ==========================================
        # RESULTADO PHISHING
        # ==========================================

        if prediction[0] == 1:

            st.error(

                "🚨 Este correo es PHISHING"

            )

            st.write(

                f"Probabilidad de phishing: "
                f"{probability[0][1] * 100:.2f}%"

            )

            st.write(

                f"Palabras sospechosas detectadas: "
                f"{suspicious_count}"

            )

        # ==========================================
        # RESULTADO LEGÍTIMO
        # ==========================================

        else:

            st.success(

                "✅ Este correo es LEGÍTIMO"

            )

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
    "Detección de Correos Phishing"

)