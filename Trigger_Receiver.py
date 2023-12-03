import pylsl

def esperar_texto():
    # Crear un objeto de entrada para el canal "LSL_triggers"
    print("Resolving Stream")
    canales = pylsl.resolve_stream('name', 'NeuroVR')
    #canales = pylsl.resolve_stream('name', 'AURA_Filtered')
    entrada = pylsl.StreamInlet(canales[0])

    print("Esperando texto desde otro programa...")

    while True:
        # Esperar la llegada de datos
        muestras, _ = entrada.pull_sample()

        # Obtener el texto recibido
        texto = muestras[0]
#        print(muestras)

        # Mostrar el texto en la consola
        #print("Texto recibido: " + texto)

esperar_texto()
