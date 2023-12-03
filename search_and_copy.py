import os
import shutil

def search_and_copy(directory):
    # replace with your specific directory
#    directory = '/path/to/your/folder'
#    directory = 'participants/Artemisa'
    
    source=""
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and 'kitchen' in filename:
            source = os.path.join(directory, filename)
#            destination = os.path.join(directory, "kitchen.csv")
 #           shutil.copyfile(source, destination)
  #          print(f'File {filename} has been copied as kitchen.csv')
            break
    else:
        print('No CSV file containing "kitchen" found in the directory')
    return source
    
#search_and_copy()
