import pylsl
import numpy as np
from pylsl import StreamInlet
import pandas as pd
import joblib
import threading

# Variable global para almacenar la predicción
prediction_data = None

# Definir funciones
def calcular_features(sample_array, columnas_a_eliminar):
    # Eliminar columnas no deseadas y calcular características
    sample_array = np.delete(sample_array, columnas_a_eliminar)
    std = np.std(sample_array)
    mean = np.mean(sample_array)
    asymmetry = pd.Series(sample_array).skew()
    return mean, std, asymmetry

def realizar_prediccion(features):
    # Convertir las características en un DataFrame con nombres de columnas
    feature_names = ['Mean', 'STD', 'Asymmetry']
    features_df = pd.DataFrame([features], columns=feature_names)

    # Hacer la predicción utilizando el modelo cargado
    prediction = model.predict(features_df)
    print("Predicción:", prediction)
    return prediction

# Función para recibir datos
def recibir_datos(entrada):
    global detener_flujo, prediction_data
    columnas_a_eliminar = list(range(8, 16)) + list(range(24, 39))

    while not detener_flujo:
        sample, timestamp = entrada.pull_sample()

        # Calcular características y realizar predicción
        features = calcular_features(np.array(sample), columnas_a_eliminar)
        prediction = realizar_prediccion(features)

        # Almacenar la predicción en la variable global
        prediction_data = prediction

# Función para iniciar el flujo de datos
def iniciar_flujo():
    global detener_flujo
    detener_flujo = False

    # Resolver el stream "AURA_Power"
    canales = pylsl.resolve_stream('name', 'AURA_Power')
    print("Resolviendo Streams")

    if not canales:
        print("No se encontró el stream 'AURA_Power'. Asegúrate de que esté siendo enviado por otro programa.")
    else:
        entrada = pylsl.StreamInlet(canales[0])
        print("Esperando datos desde el stream 'AURA_Power'...")

        # Crear y iniciar un hilo para recibir datos
        global hilo_recibir
        hilo_recibir = threading.Thread(target=recibir_datos, args=(entrada,))
        hilo_recibir.start()

# Función para detener el flujo de datos
def detener_flujo():
    global detener_flujo
    detener_flujo = True

    # Esperar a que el hilo termine
    if 'hilo_recibir' in globals() and hilo_recibir.is_alive():
        hilo_recibir.join()

# Cargar el modelo desde el archivo pkl
model = joblib.load('zensync_random_forest.pkl')
