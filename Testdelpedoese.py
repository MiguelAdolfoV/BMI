import time
import pylsl

# Función para conectar al stream LSL
def conectar_stream_lsl(nombre_stream):
    streams = pylsl.resolve_stream('name', nombre_stream)
    return pylsl.StreamInlet(streams[0])

# Función principal para el control de videos
def zensync_video_carrousel_cognitive(outlet, stream_inlet):
    seconds = 10
    video_values = [0, 0, 0, 0]
    threshold = 30

    for i in range(4):
        outlet.push_sample([f"Start_video_{i+1}"])
        print(f"sending: Start_video_{i+1}")
        time.sleep(1)
        outlet.push_sample(["fadein"])
        print("sending: fadein")
        start_time = time.time()

        while time.time() - start_time < seconds:
            # Recibir datos de Cognitive Engagement
            _, datos_procesados = stream_inlet.pull_sample()

            if datos_procesados and datos_procesados[0] > threshold:
                video_values[i] += 1

        outlet.push_sample(["fadeout"])
        print("sending: fadeout")
        time.sleep(2)

    max_value = max(video_values)
    max_index = video_values.index(max_value) + 1
    video_to_play = f"Start_video_{max_index}"
    print(f"sending: {video_to_play}")   
    outlet.push_sample([video_to_play])
    print(f"Enviando a través del outlet: {video_to_play}")

# Conectar al stream LSL para recibir datos de Cognitive Engagement
stream_inlet_ceng = conectar_stream_lsl("CEngStream")

# Conectar al outlet (reemplazar con la conexión correcta para tu sistema de videos)
outlet_video_control = None  # Aquí deberías crear el objeto outlet adecuado

# Ejecutar la función principal
zensync_video_carrousel_cognitive(outlet_video_control, stream_inlet_ceng)
