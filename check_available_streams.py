import pylsl

def check_available_streams():
    streams = pylsl.resolve_streams()
    
    if len(streams) == 0:
        print("No streams available.")
    else:
        print("Available streams:")
        for i, stream in enumerate(streams):
            print(f"{i+1}. {stream.name()} [{stream.type()}]")
            
check_available_streams()
