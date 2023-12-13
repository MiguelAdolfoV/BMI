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

## Uso de ZenSync y Vending Machine
Para utilizar ZenSync y Vending Machine de manera efectiva, sigue estos pasos:

- Requisitos Previos
- Asegúrate de cumplir con los siguientes requisitos antes de comenzar:

- Abre una ventana de Aura con Bandpass Filter configurado en 7-13Hz y asegúrate de marcar la casilla "LSL Stream Out". Es esencial que Aura se ejecute en el mismo equipo donde se ejecutará el script de Python.

- Prepara tu proyecto de Unity para ZenSync o Vending Machine con PlayMode habilitado. Asegúrate de que la máquina que ejecuta Unity esté conectada a la misma red de Internet que Aura y el script de Python para compartir los datos LSL.

-Instala y configura la aplicación para Windows de Oculus en el equipo de Unity, con QuestLink ya establecido.

Proceso
Ejecución del Script:

- Ejecuta el script runall.py para guardar los datos leídos al final de la sesión en un archivo CSV.
Si no deseas guardar datos, ejecuta main_trigger_server_Cognitive_Training_Group.py.
Inicio de la Actividad:

- Al iniciar el script, se te solicitará un ID y el número de actividad a elegir. El número 6 corresponde a ZenSync, y el número 7 a Vending Machine.
Inicio de ZenSync:

- Al seleccionar ZenSync, el script esperará a que presiones Enter para comenzar. Inicia PlayMode en Unity para ejecutar el entorno VR de ZenSync.
Si todo se ha configurado correctamente, la pantalla cambiará de negro a gris. En este punto, puedes presionar Enter en el script de Python.
Se reproducirá un carrusel de todos los videos disponibles. Después de estos videos, se seleccionará uno mediante el procesamiento de datos de relajación y engagement cognitivo para su reproducción.
Inicio de Vending Machine:

- Al seleccionar Vending Machine, el script esperará a que presiones Enter para comenzar. Inicia PlayMode en Unity para ejecutar el entorno de la Vending Machine.
El entorno es completamente automático y procedural. Deposita los objetos solicitados en la pantalla para continuar con la actividad. La dificultad se ajustará automáticamente según el rendimiento del usuario.
La actividad no tiene temporizador ni trials. Para finalizar la sesión, presiona 'f' en el script.
