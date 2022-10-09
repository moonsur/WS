import json

with open("C:\\Users\\monsu\\WS\\pwc\\Person_Profile.json", 'r') as f:
    data = json.load(f.read())
    print(data['first_name']) 