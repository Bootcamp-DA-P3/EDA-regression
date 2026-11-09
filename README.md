# 🏥 Predicción de Costos Médicos (EDA & Regresión)

Este proyecto implementa un flujo completo de Ciencia de Datos basado en el análisis de Kaggle **[EDA + Regression](https://www.kaggle.com/code/hely333/eda-regression)**. Incluye un análisis exploratorio de datos, entrenamiento de modelos de Machine Learning y una aplicación web interactiva desarrollada con **Streamlit**.

## 📁 Contenido del Repositorio
- `app.py`: Dashboard analítico e interfaz interactiva en Streamlit.
- `edaregression.ipynb`: Cuaderno de Jupyter con el EDA y entrenamiento de modelos paso a paso.
- `insurance.csv`: Dataset original con información de costos médicos de pacientes.
- `requirements.txt`: Dependencias y librerías necesarias de Python.
- `config.toml`: Archivo de configuración visual para el tema claro de Streamlit.
- `README.md`: Documentación del proyecto.

---

## ⚡ Características Principales
- **📊 Análisis Exploratorio de Datos (EDA):** Visualización de estadísticas descriptivas, matrices de correlación y distribuciones de costos según los hábitos de los pacientes.
- **🤖 Modelos de Machine Learning:** Entrenamiento y comparación de rendimiento ($R^2$ Score) entre:
  - Regresión Lineal
  - Regresión Polinómica (Grado 2)
  - Random Forest Regressor
- **🔮 Simulador Interactivo (Streamlit):** Una interfaz web con KPIs en tiempo real, filtros dinámicos y un formulario para estimar los costos médicos de nuevos pacientes.

---

## 🛠️ Instalación y Requisitos
1. Asegúrate de tener instalado Python 3.8 o superior.
2. Abre tu terminal, sitúate dentro de la carpeta `EDA-regression` e instala las librerías necesarias ejecutando:

   pip install -r requirements.txt

---

## 🚀 Guía de Uso

### 1. Ejecutar el Dashboard Interactivo (Streamlit)
Para abrir la aplicación web en tu navegador:

   streamlit run app.py

### 2. Ejecutar el Notebook de Jupyter
Si deseas revisar o ejecutar el código paso a paso:

   jupyter notebook edaregression.ipynb
