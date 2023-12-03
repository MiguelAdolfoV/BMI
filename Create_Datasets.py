import pandas as pd

def Create_Datasets(filename):

    # Read the csv file into a pandas dataframe
#    df = pd.read_csv('kitchen.csv')
    df = pd.read_csv(filename)

#    print("The number of columns is:", len(df.columns))

    # Initiate the multitask and bmi datasets as empty lists
    multitask = []
    bmi = []

    # Initialize flags for data capture
    capture_multitask = False
    capture_bmi = False

    trial = 0
    bmi_entries=0
    multitask_entries=0

    # Loop through each row in the dataframe
    for index, row in df.iterrows():
        # Check the 42nd column for keywords and set capture flags accordingly
        if row[41] == "['open_scene']":
            trial += 1
            print("Collecting Trial " + str(trial))
            capture_multitask = True
        elif row[41] == "['activate_pot_sound']":
#            print(str(multitask_entries)+" multitask entries")
            multitask_entries=0
            capture_multitask = False
            capture_bmi = True
            continue  # skip adding this row to any dataset
        elif row[41] == "['close_scene']":
#            print(str(bmi_entries)+ " bmi entries")
            bmi_entries=0
            capture_bmi = False

        # Add the row to corresponding dataset based on capture flags
        if capture_multitask:
            multitask.append(row)
            multitask_entries=multitask_entries+1
        elif capture_bmi:
            bmi.append(row)
            bmi_entries=bmi_entries+1


    # Convert the lists to dataframes using pandas.concat
    multitask = pd.concat(multitask, axis=1).transpose()
    bmi = pd.concat(bmi, axis=1).transpose()

    # Remove the 1st and last columns from each dataframe
    multitask = multitask.iloc[:, 1:-2]
    bmi = bmi.iloc[:, 1:-2]

    # Save the resultant dataframes to csv files
    multitask.to_csv('multitask.csv', index=False)
    bmi.to_csv('bmi.csv', index=False)
