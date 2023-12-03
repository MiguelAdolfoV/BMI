import pylsl
import csv
import os
from datetime import datetime
from BMI_Calibration import *
import numpy as np
from pylsl import StreamInfo, StreamOutlet


# Create a new StreamInfo
info = StreamInfo('kitchen_triggers', 'triggers', 1, 0, 'string', 'myuidw43536')
#info = StreamInfo('kitchen_triggers', 'Markers', 1, 0, 'string', 'myuidw43536')

# Create a new outlet
outlet = StreamOutlet(info)

# Resolver el stream "AURA_Power"
canales = pylsl.resolve_stream('name', 'AURA_Power')
print("Resolviendo Streams")

if len(canales) == 0:
    print("No se encontró el stream 'AURA_Power'. Asegúrate de que esté siendo enviado por otro programa.")

entrada = pylsl.StreamInlet(canales[0])
print("Esperando datos desde el stream 'AURA_Power'...")

model= BMI_Calibration('kitchen.csv')

sample_list = []
while True:
    sample, timestamp = entrada.pull_sample()
    sample_list.append(sample)

    if len(sample_list) >= 175:
        # convert list of samples into a 2D numpy array
        data_array = np.array(sample_list)

        # compute the average of the samples
        avg_sample = np.mean(data_array, axis=0)

        # reshape the averaged sample
        avg_sample = avg_sample.reshape(1, -1)
        #print(avg_sample)

        # feed the averaged sample into the model and print the prediction
        result=model.predict(avg_sample)
        print(str(result[0]))
#        outlet.push_sample([str(result)])  # start_trial
        outlet.push_sample([str(result[0])])  # start_trial

        # clear the sample list to start collecting next 175 samples
        sample_list = []


