import time
from pylsl import StreamInfo, StreamOutlet
from getpass import getpass
import keyboard
from search_and_copy import *
import random
import pylsl
import numpy as np
import pandas as pd
import joblib

info = StreamInfo('neuro_vr_triggers', 'triggers', 1, 0, 'string', 'myuidw43536')
outlet = StreamOutlet(info)
reading_keyboard=False
backspace_num=0
directory = 'participants/'
participation_id=""
script_path = 'BMI_Control_Sender.py'
model = joblib.load('zensync_random_forest.pkl') 
canales = pylsl.resolve_stream('name', 'AURA_Power')
print("Resolviendo Streams")

if not canales:
    print("No se encontró el stream 'AURA_Power'. Asegúrate de que esté siendo enviado por otro programa.")
else:
    entrada = pylsl.StreamInlet(canales[-1])
    columnas_a_eliminar = list(range(8, 16)) + list(range(24, 39))

def calcular_features(sample_array, columnas_a_eliminar):
    sample_array = np.delete(sample_array, columnas_a_eliminar)
    std = np.std(sample_array)
    mean = np.mean(sample_array)
    asymmetry = pd.Series(sample_array).skew()
    return mean, std, asymmetry

def realizar_prediccion(features):
    feature_names = ['Mean', 'STD', 'Asymmetry']
    features_df = pd.DataFrame([features], columns=feature_names)
    prediction = model.predict(features_df)
    return prediction

def calcular_cognitive_engagement(df_real_time):
    betas = df_real_time.iloc[:, 3::5].mean(axis=1)
    alphas = df_real_time.iloc[:, 2::5].mean(axis=1)
    thetas = df_real_time.iloc[:, 1::5].mean(axis=1)
    df_real_time['CEng'] = betas / (alphas + thetas)
    return df_real_time

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
    print("6. ZenSync: Relaxation Pod")
    print("7. Vending Machine: Cognitive Flexibility")
    print("8. Exit")
    print("****************************************")
    option = int(input("Option: "))
    return option

def zensync_video_carrousel_relaxation():
    seconds = 40
    video_values = [0, 0, 0, 0]
    for i in range(4):
        outlet.push_sample([f"Start_video_{i+1}"])
        print(f"sending: Start_video_{i+1}")
        time.sleep(1)
        outlet.push_sample(["fadein"])
        print("sending: fadein")
        start_time = time.time()
        while time.time() - start_time < seconds:
            sample, timestamp = entrada.pull_sample()
            features = calcular_features(np.array(sample), columnas_a_eliminar)
            prediction = realizar_prediccion(features)  
            print("Predicción de relajación: ", prediction)
            if prediction == 1:  
                video_values[i] += 1  
        outlet.push_sample(["fadeout"])
        print("sending: fadeout")
        time.sleep(2)
    for i, value in enumerate(video_values, start=1):
        print(f"Video {i} Value: {value}")
    max_value = max(video_values)
    max_index = video_values.index(max_value) + 1
    video_to_play = f"Start_video_{max_index}"
    print(f"sending: Start_video_{max_index}")
    outlet.push_sample([video_to_play])
    print(f"Enviando a través del outlet: {video_to_play}")
    outlet.push_sample(["fadein"])
    print("sending: fadein")
    outlet.push_sample(["end_trial"])
    print("sending: end_trial")

def zensync_relaxation():
    global directory
    print("**** Calibration Stage ****")
    trials = int(input("How many trials? "))
    print("Press Enter to start zensync Calibration session...")
    input()  # Wait for user input
    outlet.push_sample(["start_session:zensync"])  # start_experiment
    print("sending: start_session:zensync")    
    for i in range(trials):
        outlet.push_sample(["fadeout"])
        print("sending: fadeout")
        time.sleep(2)
        print("----> Trial: " + str(i + 1))

        zensync_video_carrousel_relaxation()
    outlet.push_sample(["end_session:zensync"])  # stop_experiment
    print("sending: end_session:zensync")
    print("End zensync Calibration routine")

def vending_machine_flexible():
    global directory
    print("Press Enter to start Vending Machine session...")
    input()
    outlet.push_sample(["start_session:vending_machine"])
    print("sending: start_session:vending_machine")    
    CEV = 0
    CEPoints = 0
    successes = 0
    failures = 0
    Threshold = 30
    while True:
        CEV = random.randint(0, 50)
        print(f"CEV actual: {CEV}")
        if CEV > Threshold:
            CEPoints += 1
            print(f"CEPoints incrementado a {CEPoints}")
    print("sending: end_session:vending_machine")
    print("End vending_machine routine")

def confirm_experiment():
    ans = input("Do you want start_experiment? (y/n): ")
    if ans.lower() == 'y':
        return ans.lower()
    elif ans.lower() == 'n':
        print("Terminating program...")
        return ans.lower()
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
    if option == 6:
        print("You selected: Egg: Attention")
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
    elif option == 8:
        print("Terminating program")
        outlet.push_sample(["exit"])
        time.sleep(2)
        break
    else:
        print("Invalid option. Please select a number between 1 and 8.")
