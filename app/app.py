
import streamlit as st
import joblib
import re
import time
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="PhishGuard",
    layout="wide"
)

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#050505,#0d1b2a,#000000);
    color:white;
}
.main-title{
    text-align:center;
    font-size:3rem;
    font-weight:bold;
    color:#00d4ff;
}
.card{
    background:#111;
    padding:20px;
    border-radius:12px;
    border:1px solid #00d4ff;
}
</style>
""", unsafe_allow_html=True)

if "historial" not in st.session_state:
    st.session_state.historial = []

with st.sidebar:
    st.title("PhishGuard")
    st.write("Detector de phishing basado en Machine Learning")
    st.divider()
    st.write("Tecnologías")
    st.write("- Streamlit")
    st.write("- Scikit-Learn")
    st.write("- Naive Bayes")

model = joblib.load("models/modelo.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

st.markdown('<p class="main-title">PhishGuard</p>', unsafe_allow_html=True)

email_text = st.text_area("Contenido del correo", height=250)

if st.button("Analizar Correo"):

    if email_text.strip():
        with st.spinner("Analizando..."):
            time.sleep(1)

        original = email_text

        urls = re.findall(r'https?://\S+', original)

        clean = email_text.lower()
        clean = re.sub(r'http\S+', '', clean)
        clean = re.sub(r'[^a-zA-Z\s]', '', clean)

        vec = vectorizer.transform([clean])

        prediction = model.predict(vec)
        probability = model.predict_proba(vec)

        riesgo = float(probability[0][1])

        st.subheader("Resultado")

        if prediction[0] == 1:
            st.error("Correo clasificado como PHISHING")
        else:
            st.success("Correo clasificado como LEGÍTIMO")

        st.progress(riesgo)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Riesgo", f"{riesgo*100:.1f}%")

        with c2:
            st.metric("URLs Detectadas", len(urls))

        with c3:
            st.metric(
                "Confianza",
                f"{max(probability[0])*100:.1f}%"
            )

        fig = px.pie(
            values=[
                probability[0][1]*100,
                probability[0][0]*100
            ],
            names=["Phishing", "Legítimo"],
            title="Distribución"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.session_state.historial.append({
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "riesgo": round(riesgo*100,2)
        })

if st.session_state.historial:
    st.subheader("Historial")
    st.dataframe(pd.DataFrame(st.session_state.historial))

st.caption("Proyecto de Machine Learning - PhishGuard")
