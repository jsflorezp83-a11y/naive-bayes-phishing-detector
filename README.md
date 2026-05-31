# PhishGuard

## Descripción

Este proyecto consiste en una aplicación web basada en Machine Learning diseñada para detectar correos electrónicos phishing utilizando el algoritmo Naive Bayes.

La aplicación analiza el contenido de un correo electrónico y predice si se trata de un mensaje legítimo o de phishing. El objetivo principal es ayudar a los usuarios a identificar posibles amenazas y aumentar la seguridad informática.

El proyecto fue desarrollado como parte de la actividad de Inteligencia Artificial I enfocada en el despliegue de modelos de Machine Learning en entornos reales.

---

## Demostración

### URL de la aplicación desplegada

https://naive-bayes-phishing-detector-evqszgq7quuxhjfxz7vg3d.streamlit.app/

### URL del repositorio

https://github.com/jsflorezp83-a11y/naive-bayes-phishing-detector.git

---

## Algoritmo utilizado

### Naive bayes

Naive Bayes es un algoritmo probabilístico de Machine Learning utilizado comúnmente en tareas de clasificación como:

- Detección de spam.
- Detección de phishing.
- Clasificación de texto.

### ¿Por qué se eligió Naive Bayes?

El algoritmo fue seleccionado porque:

- Tiene buen rendimiento en problemas de clasificación.
- Es rápido y eficiente.
- Funciona bien con datasets relacionados con phishing.
- Maneja grandes cantidades de datos.
- Es ampliamente usado en aplicaciones de ciberseguridad.

### Métricas del modelo

- Accuracy: 92%
- Precision: 90%
- Recall: 91%
- F1-Score: 90%

---

## Dataset Utilizado

### Fuente de los datos

Phishing email dataset - Kaggle

https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

### Tamaño del dataset

El dataset contiene aproximadamente 82.500 registros correspondientes a correos electrónicos utilizados para entrenar y evaluar el modelo de clasificación.

### Descripción

El conjunto de datos contiene correos electrónicos clasificados en dos categorías:

- Phishing.
- Safe email (Correo legítimo).

Este dataset fue utilizado para entrenar y evaluar el modelo de clasificación.

### Características utilizadas

- Contenido textual del correo.
- Palabras sospechosas.
- Frecuencia de términos.
- Patrones lingüísticos.
- Indicadores comunes de ataques phishing.

### Objetivo

Entrenar un modelo capaz de identificar automáticamente correos electrónicos maliciosos y diferenciarlos de correos legítimos.

---

## Tecnologías utilizadas

- Python
- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- Joblib
- Git
- GitHub

---

## Instalación local

### Requisitos

Antes de ejecutar el proyecto, asegúrese de tener instalado:

- Python 3.11 o superior.
- Pip (administrador de paquetes de Python).
- Git.
- Conexión a Internet para descargar las dependencias.

### Verificar python

```bash
python --version
```

Debería mostrar una versión igual o superior a Python 3.11.

### Verificar git

```bash
git --version
```

---

## Pasos a seguir

### 1. Clonar el repositorio

Abra una terminal o consola de comandos y ejecute:

```bash
git clone https://github.com/jsflorezp83-a11y/naive-bayes-phishing-detector.git
```

Este comando descargará una copia completa del proyecto desde GitHub a su equipo local.

### 2. Acceder al directorio del proyecto

Una vez finalizada la descarga, ingrese a la carpeta del proyecto:

```bash
cd naive-bayes-phishing-detector
```

### 3. Instalar las dependencias

Instale todas las librerías necesarias para ejecutar la aplicación:

```bash
pip install -r requirements.txt
```

Este comando instalará automáticamente todas las dependencias definidas en el archivo `requirements.txt`, incluyendo:

- Streamlit
- Scikit-Learn
- Pandas
- NumPy
- Joblib
- Matplotlib

### 4. Ejecutar la aplicación

Una vez completada la instalación, inicie la aplicación mediante:

```bash
streamlit run app/app.py
```

### 5. Acceder a la aplicación

Después de ejecutar el comando anterior, Streamlit abrirá automáticamente la aplicación en el navegador.

Si no se abre automáticamente, copie y pegue en su navegador la siguiente dirección:

```text
http://localhost:8501
```

---

## Funcionalidades

- Clasificación automática de correos electrónicos.
- Detección de intentos de phishing.
- Predicciones en tiempo real.
- Interfaz amigable para el usuario.
- Implementación de Machine Learning aplicada a la ciberseguridad.

---

## Autores

- Camilo González
- Jhontan Florez
- Miguel Rojas

---
