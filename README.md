# Naive bayes phishing detector

## Descripción  
Este proyecto consiste en una aplicación web basada en Machine Learning diseñada para detectar sitios web phishing y URLs sospechosas utilizando el algoritmo Naive Bayes.
La aplicación analiza diferentes características de una URL y predice si el sitio es legítimo o phishing. El objetivo principal es ayudar a los usuarios a identificar páginas potencialmente peligrosas y aumentar la seguridad informática.
El proyecto fue desarrollado como parte de la actividad de Inteligencia Artificial I enfocada en el despliegue de modelos de Machine Learning en entornos reales.

## Demostración
URL de la aplicacion desplegada:()
URL del repositorio: [https://github.com/jsflorezp83-a11y/naive-bayes-phishing-detector.git]

## Algoritmo utilizado 
Naive bayes

Naive Bayes es un algoritmo probabilístico de Machine Learning utilizado comúnmente en tareas de clasificación como:

-detección de spam
-detección de phishing
-clasificación de texto

¿Por qué se eligió Naive Bayes?

El algoritmo fue seleccionado porque:

-Tiene buen rendimiento en problemas de clasificación
-Es rápido y eficiente
-Funciona bien con datasets relacionados con phishing
-Maneja grandes cantidades de datos
-Es ampliamente usado en aplicaciones de ciberseguridad

Métricas del Modelo
Accuracy: 92%
Precision: 90%
Recall: 91%
F1-Score: 90%

## Dataset utilizado 

Fuente de los datos:

Phishing Email Dataset - Kaggle
https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

Tamaño del dataset:
El dataset tiene un tamaño de 82.500 datos introducidos que en este caso son de correos electronicos de una empresa real.

Descripción

El conjunto de datos contiene correos electrónicos clasificados en dos categorías:

-Phishing
-Safe Email (Correo legítimo)

Este dataset fue utilizado para entrenar y evaluar el modelo de clasificación.

Características utilizadas

-Contenido textual del correo.
-Palabras sospechosas.
-Frecuencia de términos.
-Patrones lingüísticos.
-Indicadores comunes de ataques phishing.
-Objetivo

Entrenar un modelo capaz de identificar automáticamente correos electrónicos maliciosos y diferenciarlos de correos legítimos.

Tecnologías Utilizadas:
-Python
-Streamlit
-Scikit-Learn
-Pandas
-NumPy
-Joblib
-Git
-GitHub

## Instalación local 

## Requisitos
Antes de ejecutar el proyecto, asegúrese de tener instalado:

-Python 3.11 o superior
-Pip (administrador de paquetes de Python)
-Git

Una conexión a Internet para descargar las dependencias
Para verificar que Python está instalado correctamente, ejecute:
python --version
Debería mostrar una versión igual o superior a Python 3.11.

Para verificar Git:
git --version

### Pasos a seguir 

1. Clonar el Repositorio:
Abra una terminal o consola de comandos y ejecute:
git clone https://github.com/jsflorezp83-a11y/naive-bayes-phishing-detector.git
Este comando descargará una copia completa del proyecto desde GitHub a su equipo local.

2. Acceder al Directorio del Proyecto:
Una vez finalizada la descarga, ingrese a la carpeta del proyecto:
cd naive-bayes-phishing-detector

3. Instalar las Dependencias

Instale todas las librerías necesarias para ejecutar la aplicación:
-pip install -r requirements.txt

Este comando instalará automáticamente todas las dependencias definidas en el archivo requirements.txt, incluyendo:

-Streamlit
-Scikit-Learn
-Pandas
-NumPy
-Joblib
-Matplotlib

4. Ejecutar la Aplicación

Una vez completada la instalación, inicie la aplicación mediante:
streamlit run app/app.py

5. Acceder a la Aplicación

Después de ejecutar el comando anterior, Streamlit abrirá automáticamente la aplicación en el navegador.
Si no se abre automáticamente, copie y pegue en su navegador la URL mostrada en la terminal, normalmente:

http://localhost:8501

