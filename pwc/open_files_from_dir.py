import os
path = 'C:\\Users\\monsu\\WS'
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        full_path = path +'\\'+ filename
        print(full_path)
        with open(full_path,'r') as f:
            print(f.read())