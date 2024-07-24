# Despliegue del modelo ML
Generaremos un modelo SVM y lo pondremos en producción usando Streamlit. El modelo SVM permitirá predecir si obtendrá ganancias superies o inferiores a 50K.

##  1. Entrenamiento del modelo
Entrenamos diferentes modelos, como Regresión Logística, SVM (Con 4 kernels), Árboles de Decisión, K-nn, Bayes y RNA. Los cuales se pueden encontrar dentro de la carpeta de ´´entrenamiento´´

##  2. Producción en servidor local - preparación del entorno

Creamos un entorno con python 3.7, e instalamos las dependencias necesarias.

    $   conda create -n ApiCrop
    $   conda activate ApiCrop
    $   conda install python=3.7
    $   cd rutaDondeGuardesEsteRepositorioDescargado
    $   pip install -r requirements.txt
    $   streamlit run app.py
    
## 3. Evidencias
    
  ![Screenshot](https://github.com/DavidReveloLuna/API_Gcloud_Streamlit/blob/master/assets/Screenshot.png)

## Agradecimientos

[Praneeth Kandula](https://medium.com/analytics-vidhya/deploying-streamlit-apps-to-google-app-engine-in-5-simple-steps-5e2e2bd5b172)
