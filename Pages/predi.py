import streamlit as st
import pandas as pd
import pickle

# Cargar el modelo y los codificadores guardados
with open('modelo_seguros.pkl', 'rb') as f:
    model = pickle.load(f)

with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

st.title("Predicción de Costes de Seguro Médicos 🏥")
st.write("Introduce los datos del cliente para estimar los cargos del seguro.")

# Crear los campos de entrada en la interfaz de Streamlit
age = st.number_input("Edad (age)", min_value=18, max_value=100, value=30)
sex = st.selectbox("Sexo (sex)", options=encoders['sex'].classes_)
bmi = st.number_input("Índice de Masa Corporal (bmi)", min_value=10.0, max_value=50.0, value=25.0)
children = st.number_input("Número de hijos (children)", min_value=0, max_value=10, value=0)
smoker = st.selectbox("¿Es fumador? (smoker)", options=encoders['smoker'].classes_)
region = st.selectbox("Región (region)", options=encoders['region'].classes_)

# Botón para realizar la predicción
if st.button("Predecir Costes"):
    # Transformar los inputs categóricos usando los LabelEncoders guardados
    sex_enc = encoders['sex'].transform([sex])[0]
    smoker_enc = encoders['smoker'].transform([smoker])[0]
    region_enc = encoders['region'].transform([region])[0]
    
    # Crear el DataFrame de entrada con el mismo orden de columnas que en el entrenamiento
    input_data = pd.DataFrame([[age, sex_enc, bmi, children, smoker_enc, region_enc]],
                              columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])
    
    # Realizar la predicción
    prediction = model.predict(input_data)[0]
    
    # Mostrar el resultado en pantalla
    st.success(f"Coste estimado: ${prediction:,.2f}")
    st.metric(label="Coste Estimado del Seguro", value=f"${prediction:,.2f}")