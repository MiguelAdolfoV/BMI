import time
from pylsl import StreamInfo, StreamOutlet
from getpass import getpass
import keyboard
from search_and_copy import *
#from RT_Engagement import ultimo_ceng
import os 
import shutil
import subprocess
import random
import pylsl
import numpy as np
import pandas as pd
import joblib
import RT_Engagement
import threading


# Create a new StreamInfo
info = StreamInfo('neuro_vr_triggers', 'triggers', 1, 0, 'string', 'myuidw43536')

# Create a new outlet
outlet = StreamOutlet(info)

reading_keyboard=False
backspace_num=0

directory = 'participants/'

participation_id=""

script_path = 'BMI_Control_Sender.py'

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
    #print("Predicción:", prediction)
    return prediction

# Cargar el modelo desde el archivo pkl
model = joblib.load('zensync_random_forest.pkl') 

# Resolver el stream "AURA_Power"
canales = pylsl.resolve_stream('name', 'AURA_Power')
print("Resolviendo Streams")

if not canales:
    print("No se encontró el stream 'AURA_Power'. Asegúrate de que esté siendo enviado por otro programa.")
else:
    entrada = pylsl.StreamInlet(canales[-1])
    print("Esperando datos desde el stream 'AURA_Power'...")

    # Columnas a eliminar
    columnas_a_eliminar = list(range(8, 16)) + list(range(24, 39))

def read_keyboard(event):
    global backspace_num
    if reading_keyboard==True:
        tecla = event.name
        if tecla in [str(i) for i in range(1, 10)]:
            tecla="trigger_"+tecla        
        outlet.push_sample([tecla])
        print("Trigger sent: "+tecla)
        backspace_num=backspace_num+1

def delete_typed_keys():
    global backspace_num
    for _ in range(backspace_num):
        keyboard.press_and_release('backspace')
    backspace_num=0

def display_menu():
    print("***************** Cognitive Training Menu *****************")
    print("Select excercise")
    print("1. Egg: Attention")
    print("2. Theater: Working Memory")
    print("3. Mole: Control and Inhibition")
    print("4. Lab: Multitasking")
    print("5. Kitchen: Multitasking + BMI")
    print("6. ZenSync: Relaxation Pod")
    print("7. Vending Machine: Cognitive Flexibility")
    print("8. Exit")
    print("****************************************")
    option = int(input("Option: "))
    return option

# Send words function
def theater_trial_routine():
    outlet.push_sample(["start_trial"])  # start_trial
    print("sending: start_trial")
    #time.sleep(1)
    outlet.push_sample(["open_curtain"])  # start_trial
    print("sending: open_curtain")
    time.sleep(10)
    outlet.push_sample(["close_curtain"])  # sound_pot
    print("sending: close_curtain")    
    time.sleep(12)
    outlet.push_sample(["start_performing_task"])  # sound_pot
    print("sending: perform_task")    
    time.sleep(20)
    outlet.push_sample(["open_curtain"])  # sound_pot
    print("sending: open_curtain")    
    time.sleep(7)    
    outlet.push_sample(["close_curtain2"])  # sound_pot
    print("sending: close_curtain2")    
    time.sleep(1)
    outlet.push_sample(["end_trial"])  # end_trial
    print("sending: end_trial")
    #time.sleep(1)

def kitchen_trial_routine():
    outlet.push_sample(["start_trial"])  # start_trial
    print("sending: start_trial")
    time.sleep(2)
    outlet.push_sample(["open_scene"])  # start_trial
    print("sending: open_scene")
    time.sleep(10)
    outlet.push_sample(["activate_pot_sound"])  # sound_pot
    print("sending: activate_pot_sound")    
    time.sleep(10)
    outlet.push_sample(["close_scene"])  # start_trial
    print("sending: close_scene")
    time.sleep(1) 
    outlet.push_sample(["end_trial"])  # end_trial
    print("sending: end_trial")
    time.sleep(2)

def theather_memory():
    trials = int(input("How many trials? "))
    print("Press Enter to start Theater session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:theater"])  # start_experiment
    print("sending: start_session:theater")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        theater_trial_routine()

    outlet.push_sample(["end_session:theater"])  # start_experiment
    print("sending: end_session:theater")
    print("End theather_memory routine")

def kitchen_multitasking_bmi():
    global directory
    print("**** Calibration Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start Kitchen Calibration session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:kitchen"])  # start_experiment
    print("sending: start_session:kitchen")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        kitchen_trial_routine()
    outlet.push_sample(["end_session:kitchen"])  # start_experiment
    print("sending: end_session:kitchen")
    print("End kitchen Calibration routine")

    directory=os.path.join(directory,participation_id)
    source_filename=search_and_copy(directory)
    print(source_filename)
    shutil.copyfile(source_filename, "kitchen.csv")
    print(f'File {source_filename} has been copied as kitchen.csv')

    #Start Calibration and Execution
    print("*****Launching BMI Control Sender ****")
    time.sleep(2)
    subprocess.Popen(f'start cmd.exe @cmd /k python {script_path}', shell=True)

    # repeat Kitchen scene
    print("**** Evaluation Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start Kitchen Evaluation session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:kitchen_evaluation"])  # start_experiment
    print("sending: start_session:kitchen_evaluation")    
    for i in range(trials):
        print("----> Trial: "+str(i+1))
        kitchen_trial_routine()
    outlet.push_sample(["end_session:kitchen_evaluation"])  # start_experiment
    print("sending: end_session:kitchen_evaluation")
    print("End kitchen Calibration routine")

def tent_relaxation():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Tent session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:tent"])  # start_experiment
    print("sending: session_tent_relaxation")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(10)
    outlet.push_sample(["end_session:tent"])  # start_experiment
    print("sending: end_session:tent")
    print("End tent_relaxation routine")

def mole_control_inhibition():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Mole session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:mole"])  # start_experiment
    print("sending: start_session:mole")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(60)
    outlet.push_sample(["end_session:mole"])  # start_experiment
    print("sending: end_session:mole")
    print("End mole_control_inhibition routine")

def lab_multitasking():
    mins = int(input("How many minutes? "))
    print("Press Enter to start Lab session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:lab"])  # start_experiment
    print("sending: start_session:lab")    
    for i in range(mins):
        print("----> Min "+str(i+1))
        time.sleep(60)
    outlet.push_sample(["end_session:lab"])  # start_experiment
    print("sending: end_session:lab")
    print("End lab_multitasking routine")

def zensync_video_carrousel():
    seconds = 5
    video_values = [0, 0, 0, 0, 0]  # video_1_value, video_2_value, video_3_value, video_4_value
    cognitive_values = [0, 0, 0, 0, 0]  # video_1_value, video_2_value, video_3_value, video_4_value
    thread = threading.Thread(target=RT_Engagement.procesar_datos_eternamente)
    thread.start()
    # Código para manejar el stream LSL
    
    for i in range(5):
        # Comenzar cada video
        outlet.push_sample([f"Start_video_{i+1}"])
        print(f"sending: Start_video_{i+1}")
        time.sleep(1)
        outlet.push_sample(["fadein"])
        print("sending: fadein")
        start_time = time.time()
        contadorInicial = RT_Engagement.contador
        # Procesar muestras de IA durante el video
        while time.time() - start_time < seconds:
            sample, timestamp = entrada.pull_sample()

            # Calcular características y realizar predicción
            features = calcular_features(np.array(sample), columnas_a_eliminar)
            prediction = realizar_prediccion(features)
            pred = prediction
            if pred == 1:
                video_values[i] += 1

        contadorFinal = RT_Engagement.contador
        numeros_en_rango = [i for i in range(contadorInicial, contadorFinal + 1)]
        cognitive_values[i] = sum(numeros_en_rango)
        outlet.push_sample(["fadeout"])
        print("sending: fadeout")
        time.sleep(2)
        
    # Imprimir los valores finales para cada video
    for i, value in enumerate(video_values, start=1):
        print(f"Relaxation video {i} Value: {value}")

    for i, value in enumerate(cognitive_values, start=1):
        print(f"Cognitive video {i} Value: {value}")

    # Determinar la posición con la mayor suma de valores
    suma_valores = [x + y for x, y in zip(video_values, cognitive_values)]
    max_suma = max(suma_valores)
    max_suma_index = suma_valores.index(max_suma) + 1  # +1 porque los índices comienzan en 0

    # Obtener los nombres de los videos con mayor valor
    video_to_play_video = f"Start_video_{max_suma_index}"

    print(f"Sending: {video_to_play_video}")

    # Enviar el nombre del video con mayor suma al outlet
    outlet.push_sample([video_to_play_video])
    print(f"Enviando a través del outlet: {video_to_play_video}")
    outlet.push_sample(["fadein"])
    print("sending: fadein")

    outlet.push_sample(["end_trial"])
    print("sending: end_trial")    

def zensync_relaxation():
    global directory
    print("**** Calibration Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start zensync session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:zensync"])  # start_experiment
    print("sending: start_session:zensync")    
    outlet.push_sample(["fadeout"])
    print("sending: fadeout")
    time.sleep(2)
    zensync_video_carrousel()
    outlet.push_sample(["end_session:zensync"])  # stop_experiment
    print("sending: end_session:zensync")
    print("End zensync Calibration routine")
    
def vending_machine_flexible():
    global directory  # Asegúrate de que la variable 'directory' está definida

    print("To stop the session, press the F key after starting the session")
    print("Press Enter to start Vending Machine session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:vending_machine"])  # start_experiment
    print("sending: start_session:vending_machine")

    thread = threading.Thread(target=RT_Engagement.procesar_datos_eternamente)
    thread.start()

    while True:
        sample_value = str(RT_Engagement.contador)  # Convertir a cadena
        outlet.push_sample([sample_value])  # stop_experiment
        print(sample_value)

        # Salir del bucle si la tecla "f" está presionada
        if keyboard.is_pressed('f'):
            break

    print("Ending session")
    outlet.push_sample(["end_session:vending_machine"])  # stop_experiment
    print("sending: end_session:vending_machine")
    print("End vending_machine Calibration routine")

def egg_attention():
    global reading_keyboard
    mins = int(input("How many minutes? "))
    print("Press Enter to start Egg session...")
    input()  # Wait for user input
    reading_keyboard=True
    keyboard.on_press(read_keyboard)    
    outlet.push_sample(["start_session:egg"])  # start_experiment
    print("sending: session_egg_attention")
    for i in range(mins):
        print("----> Min "+str(i+1))        
        time.sleep(60)
    outlet.push_sample(["end_session:egg"])  # start_experiment
    print("sending: end_session:egg")
    print("End egg_attention routine")
    reading_keyboard=False
    delete_typed_keys()

def confirm_experiment():
    ans = input("Do you want start_experiment? (y/n): ")
    if ans.lower() == 'y':
        return ans.lower()
    elif ans.lower() == 'n':
        return ans.lower()
        #print("Terminating program...")
    else:
        print("Invalid input, please enter 'y' for yes or 'n' for no.")

def get_send_participant_code():
    global participation_id
    while True:
        code = input("Type participant ID: ")
        participation_id=code
        code_trigger="participant_id:"+str(code)        
        print("ID entered:"+code_trigger)
        ans = input("is the ID correct? (y/n): ")
        if ans.lower() == 'y':
            outlet.push_sample([code_trigger])
            print(code_trigger+" sent")
            break
        elif ans.lower() == 'n':
            continue
        else:
            print("Invalid input, please enter 'y' for yes or 'n' for no.")

def break_rest():
    mins = 2
    print("********************Start Break ********************")    
    for i in range(mins):
        print("Break ----> Min "+str(i+1))
        time.sleep(60)
    print("********************End Break ********************")    

print("...Main Experiment LSL Server Started...")

get_send_participant_code()

while True:

    option=display_menu()


    if option == 1:
        print("You selected: Egg: Attention")
        confirmation=confirm_experiment()
        if confirmation=='y':
            egg_attention()
            break_rest()
        else:
            print("Going back to menu...")        
    elif option == 2:
        print("You selected: Theater: Working Memory")
        confirmation=confirm_experiment()
        if confirmation=='y':
            theather_memory()
            break_rest()
        else:
            print("Going back to menu...")        
    elif option == 3:
        print("You selected: Mole: Control and Inhibition")
        confirmation=confirm_experiment()
        if confirmation=='y':
            mole_control_inhibition()
            break_rest()
        else:
            print("Going back to menu...")             
    elif option == 4:
        print("You selected: Lab: Multitasking")
        confirmation=confirm_experiment()
        if confirmation=='y':
            lab_multitasking()
            break_rest()
        else:
            print("Going back to menu...")           
    elif option == 5:
        print("You selected: Kitchen: Multitasking + BMI")
        confirmation=confirm_experiment()
        if confirmation=='y':
            kitchen_multitasking_bmi()
            #break_rest()
        else:
            print("Going back to menu...")          
    elif option == 6:
        print("You selected: ZenSync: Relaxation Pod")
        confirmation=confirm_experiment()
        if confirmation=='y':
            zensync_relaxation()
            #break_rest()
        else:
            print("Going back to menu...")          
    elif option == 7:
        print("You selected: Vending Machine: Cognitive Flexibility")
        confirmation=confirm_experiment()
        if confirmation=='y':
            vending_machine_flexible()
            #break_rest()
        else:
            print("Going back to menu...")          
    elif option == 8:
        print("Terminating program")
        outlet.push_sample(["exit"])
        time.sleep(2)
        break
    else:
        print("Invalid option. Please select a number between 1 and 8.")
