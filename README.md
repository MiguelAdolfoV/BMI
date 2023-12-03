# Cognitive Engagement EEG

## Descripción
Este proyecto está diseñado para medir el compromiso cognitivo en tiempo real utilizando datos EEG. Utiliza la biblioteca Lab Streaming Layer (LSL) para recibir datos de EEG y procesarlos para calcular el compromiso cognitivo basado en las bandas de frecuencia Alpha, Beta y Theta.

## Características
- Conexión en tiempo real con streams EEG utilizando LSL.
- Cálculo del compromiso cognitivo a partir de las bandas de frecuencia Alpha, Beta y Theta.
- Visualización en tiempo real del compromiso cognitivo utilizando Matplotlib.

## Requisitos
Para ejecutar este proyecto, necesitarás Python y las siguientes bibliotecas:
- pylsl
- pandas
- numpy
- matplotlib
Necesitaras dispositivo AURA by Mirai Innovation y software de AURA para conectarte al LSL 

## Instalación
Clona este repositorio y navega al directorio del proyecto. Instala las dependencias necesarias:
git clone [url-del-repositorio]
cd [nombre-del-directorio]
pip install pylsl pandas numpy matplotlib

## Uso
Para iniciar la captura y el análisis de los datos EEG en tiempo real, ejecuta:
python RT_Engagement.py
