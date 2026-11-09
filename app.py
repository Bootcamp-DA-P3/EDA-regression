import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# Configuración de la página y forzar tema claro
st.set_page_config(page_title="Predicción de Costos Médicos - EDA & Regresión", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

plt.style.use('default')
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "text.color": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black"
})

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("insurance.csv")
    except:
        url = "https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv"
        df = pd.read_csv(url)
    return df

try:
    data = load_data()
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.stop()

st.title("🏥 Predicción de Costos Médicos (EDA y Regresión)")
st.markdown("Aplicación interactiva basada en el análisis de Kaggle **EDA + Regression**.")

# Pestañas de navegación
tab1, tab2, tab3 = st.tabs(["📊 Análisis Exploratorio (EDA)", "🤖 Modelos de Regresión", "🔮 Predicción Interactiva"])

with tab1:
    st.header("Análisis Exploratorio de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Primeras filas del Dataset")
        st.dataframe(data.head())
    with col2:
        st.subheader("Estadísticas descriptivas")
        st.write(data.describe())

    st.subheader("Matriz de Correlación")
    df_corr = data.copy()
    le_sex = LabelEncoder()
    le_smoker = LabelEncoder()
    le_region = LabelEncoder()
    
    df_corr['sex'] = le_sex.fit_transform(df_corr['sex'])
    df_corr['smoker'] = le_smoker.fit_transform(df_corr['smoker'])
    df_corr['region'] = le_region.fit_transform(df_corr['region'])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(df_corr.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    st.subheader("Distribución de Costos por Hábito de Fumar")
    fig2, ax2 = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(data[data['smoker'] == 'yes']['charges'], color='red', ax=ax2[0], kde=True)
    ax2[0].set_title('Fumadores')
    sns.histplot(data[data['smoker'] == 'no']['charges'], color='blue', ax=ax2[1], kde=True)
    ax2[1].set_title('No Fumadores')
    st.pyplot(fig2)

with tab2:
    st.header("Evaluación de Modelos de Machine Learning")
    
    X = df_corr.drop(['charges'], axis=1)
    y = df_corr['charges']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

    # 1. Regresión Lineal
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_score = lr.score(X_test, y_test)

    # 2. Regresión Polinómica
    quad = PolynomialFeatures(degree=2)
    X_quad = quad.fit_transform(X.drop(['region'], axis=1))
    X_train_q, X_test_q, y_train_q, y_test_q = train_test_split(X_quad, y, test_size=0.25, random_state=0)
    plr = LinearRegression()
    plr.fit(X_train_q, y_train_q)
    plr_score = plr.score(X_test_q, y_test_q)

    # 3. Random Forest
    forest = RandomForestRegressor(n_estimators=100, random_state=1, n_jobs=-1)
    forest.fit(X_train, y_train)
    forest_pred = forest.predict(X_test)
    forest_r2 = r2_score(y_test, forest_pred)

    col1, col2, col3 = st.columns(3)
    col1.metric("R² Regresión Lineal", f"{lr_score:.4f}")
    col2.metric("R² Regresión Polinómica", f"{plr_score:.4f}")
    col3.metric("R² Random Forest", f"{forest_r2:.4f}")

    st.info("La Regresión Polinómica y Random Forest muestran un mejor rendimiento al capturar relaciones no lineales en los datos.")

with tab3:
    st.header("🔮 Estima los Costos Médicos de un Paciente")
    
    with st.form("pred_form"):
        c1, c2 = st.columns(2)
        with c1:
            age = st.slider("Edad", 18, 64, 30)
            sex = st.selectbox("Sexo", ["female", "male"])
            bmi = st.number_input("Índice de Masa Corporal (IMC)", 10.0, 60.0, 25.0)
        with c2:
            children = st.number_input("Número de hijos", 0, 5, 0)
            smoker = st.selectbox("¿Fuma?", ["yes", "no"])
            region = st.selectbox("Región", ["northeast", "northwest", "southeast", "southwest"])
        
        model_type = st.selectbox("Modelo a utilizar", ["Regresión Lineal", "Regresión Polinómica", "Random Forest"])
        submitted = st.form_submit_button("Calcular Predicción")

    if submitted:
        input_df = pd.DataFrame({
            'age': [age],
            'sex': [1 if sex == 'female' else 0],
            'bmi': [bmi],
            'children': [children],
            'smoker': [1 if smoker == 'yes' else 0],
            'region': le_region.transform([region])[0]
        })

        if model_type == "Regresión Lineal":
            pred = lr.predict(input_df)[0]
        elif model_type == "Regresión Polinómica":
            input_q = quad.transform(input_df.drop(['region'], axis=1))
            pred = plr.predict(input_q)[0]
        else:
            pred = forest.predict(input_df)[0]

        st.success(f"### Costo Médico Estimado: $ {pred:,.2f} USD")