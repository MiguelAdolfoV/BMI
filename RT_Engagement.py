import pylsl
import pandas as pd
import numpy as np

def conectar_stream_lsl(nombre_stream):
    streams = pylsl.resolve_stream('name', nombre_stream)
    return pylsl.StreamInlet(streams[0])

def calcular_cognitive_engagement(df_real_time):
    betas = df_real_time.iloc[:, 3::5].mean(axis=1)
    alphas = df_real_time.iloc[:, 2::5].mean(axis=1)
    thetas = df_real_time.iloc[:, 1::5].mean(axis=1)
    df_real_time['CEng'] = betas / (alphas + thetas)
    return df_real_time

def enviar_datos_lsl(stream_outlet, dato):
    stream_outlet.push_sample([dato])

def procesar_datos_eternamente(stream_inlet):
    # Crear un outlet para enviar datos de Cognitive Engagement
    info = pylsl.StreamInfo('CEngStream', 'Engagement', 1, pylsl.IRREGULAR_RATE, 'float32', 'ceng12345')
    stream_outlet = pylsl.StreamOutlet(info)

    columnas = ['Canal' + str(i) for i in range(1, 41)]
    df_real_time = pd.DataFrame(columns=columnas)

    while True:
        muestras, timestamp = stream_inlet.pull_sample()
        if muestras:
            df_muestra = pd.DataFrame([muestras], columns=columnas)
            df_real_time = pd.concat([df_real_time, df_muestra], ignore_index=True)
            df_real_time = calcular_cognitive_engagement(df_real_time)

            # Enviar la última predicción de Cognitive Engagement
            ultimo_ceng = df_real_time['CEng'].iloc[-1]
            enviar_datos_lsl(stream_outlet, ultimo_ceng)

# Conectar al stream LSL
stream_inlet = conectar_stream_lsl("AURA_Power")

# Procesar los datos continuamente
procesar_datos_eternamente(stream_inlet)