import numpy as np
import pickle
import streamlit as st
import pandas as pd

# Path del modelo preentrenado
MODEL_PATH = 'models/svm_model_rbf.pkl'

# Se recibe la entrada y el modelo, devuelve la predicción
def model_prediction(x_in, model):
    preds = model.predict(x_in)
    return preds

def main():
    # Carga el modelo y las columnas esperadas
    with open(MODEL_PATH, 'rb') as file:
        data = pickle.load(file)
        model = data['model']
        columns = data['columns']
        label_encoders = data['label_encoders']
        scaler = data['scaler']
        income_encoder = data['income_encoder']

    if model is None:
        st.error("No se pudo cargar el modelo.")
        return

    # Título y Estilos Personalizados
    st.markdown(
        """
        <style>
        .main {
            background-color: #f0f2f6;
            color: #000;
        }
        .stButton>button {
            color: white;
            background: #4CAF50;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-size: 1.1rem;
            cursor: pointer;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }
        .stButton>button:hover {
            background: #45a049;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div>div>button {
            padding: 0.6rem;
            font-size: 1.1rem;
            color: #000;
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }
        .stSelectbox>div>div>div>button {
            padding-right: 1.2rem; /* ensure dropdown arrow is visible */
        }
        label {
            color: #000 !important;
            font-size: 1rem;
        }
        h1 {
            color: #181082;
            text-align: center;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        .stMarkdown>div>p {
            color: #000000 !important; /* negro */
            font-size: 1.1rem;
            font-weight: bold;
        }
        .stSuccess>div>p {
            color: #000 !important;
            font-size: 1.1rem;
            font-weight: bold;
        }
        .prediction-box {
            background-color: #e6ffe6;
            border: 2px solid #004d00;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            margin-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1>Sistema de Predicción de Ingresos Anuales</h1>", unsafe_allow_html=True)

    # Campos de entrada distribuidos en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Edad:", min_value=0, max_value=100, step=1)
        fnlwgt = st.number_input("Salario:", min_value=0, step=1)
        education_num = st.number_input("Años de Educación:", min_value=0, max_value=20, step=1)
        capital_gain = st.number_input("Ganancia de Capital:", min_value=0, step=1)
        capital_loss = st.number_input("Pérdida de Capital:", min_value=0, step=1)
        hours_per_week = st.number_input("Horas por Semana:", min_value=0, max_value=100, step=1)

    with col2:
        workclass = st.selectbox("Clase de Trabajo:", ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov', 'Without-pay', 'Never-worked'])
        education = st.selectbox("Educación:", ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool'])
        marital_status = st.selectbox("Estado Civil:", ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed', 'Married-spouse-absent', 'Married-AF-spouse'])
        occupation = st.selectbox("Ocupación:", ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty', 'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving', 'Priv-house-serv', 'Protective-serv', 'Armed-Forces'])
        relationship = st.selectbox("Relación Familiar:", ['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'])
        race = st.selectbox("Raza:", ['White', 'Black', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other'])
        sex = st.selectbox("Sexo:", ['Female', 'Male'])
        native_country = st.selectbox("País de Origen:", ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany', 'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba', 'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico', 'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan', 'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand', 'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands'])

    # Validar que todos los campos estén llenos y que las condiciones de edad y salario se cumplan
    if st.button("Realizar Predicción"):
        if any([age is None, fnlwgt is None, education_num is None, capital_gain is None, capital_loss is None, hours_per_week is None]):
            st.error("Por favor, complete todos los campos.")
        elif age < 18:
            st.error("La edad debe ser mayor a 18.")
        elif fnlwgt < 200:
            st.error("El salario debe ser mayor a 200.")
        else:
            # Crear el vector de entrada
            x_in = [
                age,
                workclass,
                fnlwgt,
                education,
                education_num,
                marital_status,
                occupation,
                relationship,
                race,
                sex,
                capital_gain,
                capital_loss,
                hours_per_week,
                native_country
            ]

            # Convertir a DataFrame
            input_df = pd.DataFrame([x_in], columns=['age', 'workclass', 'fnlwgt', 'education', 'education_num', 'marital_status', 'occupation', 'relationship', 'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country'])

            # Codificar variables categóricas
            for feature in label_encoders:
                if feature in input_df:
                    input_df[feature] = label_encoders[feature].transform(input_df[feature])

            # Escalar los datos de entrada
            input_df_scaled = scaler.transform(input_df)

            # Mostrar los datos de entrada
            st.write("Datos de Entrada:")
            st.dataframe(input_df)

            # Realizar la predicción
            prediction = model_prediction(input_df_scaled, model)
            prediction_decoded = income_encoder.inverse_transform(prediction)

            # Mostrar el resultado de la predicción en un cuadro centrado
            st.markdown(
                f'<div class="prediction-box"><p>Ingreso Anual: {prediction_decoded[0]}</p></div>',
                unsafe_allow_html=True
            )

if __name__ == '__main__':
    main()
