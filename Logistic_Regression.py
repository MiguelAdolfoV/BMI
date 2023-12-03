import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler


def Logistic_Regression():
	# Load the datasets
	#multitask = pd.read_csv('multitask.csv')
	#bmi = pd.read_csv('bmi.csv')
	multitask = pd.read_csv('multitask.csv').assign(Label=-1)
	bmi = pd.read_csv('bmi.csv').assign(Label=1)

	# Concatenate the datasets
	df = pd.concat([multitask, bmi])

	print("df size: "+str(df.shape))


	# Separate features and target
	X = df.iloc[:, :-1]
	y = df.iloc[:, -1]

	print("X:"+ str(X.shape))

	# Create a scaler object
	scaler = MinMaxScaler(feature_range=(-1, 1))

	#sc_x = scaler.fit_transform(X)
	X = scaler.fit_transform(X)
	print("X_train size: "+str(len(X[0])))

	# Convert the target into binary categories
#	y = pd.cut(y, bins=[y.min(), y.median(), y.max()], include_lowest=True, labels=[0, 1])


	# Split the data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	# Create a Logistic Regression model
	model = LogisticRegression(max_iter=1000)

	# Train the model
	model.fit(X_train, y_train)

	# Evaluate the model
	train_score = model.score(X_train, y_train)
	test_score = model.score(X_test, y_test)

	print("Training accuracy: ", train_score)
	print("Testing accuracy: ", test_score)
	return model 
