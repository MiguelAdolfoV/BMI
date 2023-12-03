import pylsl

def detectar_redes_lsl():
    # Imprimir un mensaje para indicar que se está buscando streams LSL
    print("Buscando streams LSL disponibles...")

    # Usar la función resolve_streams para buscar todos los streams disponibles
    streams = pylsl.resolve_streams()

    # Verificar si se encontraron streams
    if streams:
        print(f"Se encontraron {len(streams)} streams:")
        for i, stream in enumerate(streams):
            # Obtener información directamente del stream
            print(f"Stream {i + 1}:")
            print(f"  Nombre: {stream.name()}")
            print(f"  Tipo: {stream.type()}")
            print(f"  Número de canales: {stream.channel_count()}")
            print(f"  Frecuencia de muestreo: {stream.nominal_srate()}")
            print(f"  UID: {stream.uid()}")
            print(f"  Hostname: {stream.hostname()}")
    else:
        print("No se encontraron streams LSL.")

# Llamar a la función para detectar streams
detectar_redes_lsl()
