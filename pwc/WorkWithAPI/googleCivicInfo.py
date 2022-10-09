import requests
import json
from createtable import create_tables

# Create Tables if does not exists
create_tables()
key = "AIzaSyDqfPE99DZFTKO2bHaPAswJL7qyoKQQDFE"
pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Any?levels=administrativeArea1&key=[YOUR_API_KEY]" 

url = pre_url.replace("[YOUR_API_KEY]",key)


response = requests.get(url)
print(response.status_code)
print(response.text) 

data = json.loads(response.text)
# print(data)
for key, val in data.items():
    if key == "officials":
        print("this is officials")
    elif key == "offices":  
        print('this is office data')
        """ insert multiple vendors into the vendors table  """
        sql = "INSERT INTO vendors(name,divisionId,levels,roles) VALUES(%s,)"
        for office in val:  
            # print(office)    
            print('name ->', office['name'])
            print('divisionId ->', office['divisionId'])
            print('levels ->', office['levels'])
            print('roles ->', office['roles'])
            print('officialIndices ->', office['officialIndices'])
    elif key == 'divisions':
        print('this is divisions')
    print("*"*50)