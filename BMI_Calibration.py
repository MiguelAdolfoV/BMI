import csv
from Create_Datasets import *
from Logistic_Regression import *

def BMI_Calibration(filename):
	print("*** Creating Datasets ***")
	Create_Datasets(filename)
	print("*** Trining Logistic Regression ***")
	model = Logistic_Regression()

	return model


