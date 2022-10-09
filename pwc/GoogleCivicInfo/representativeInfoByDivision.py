import requests
import json
from createtable import create_tables
from dataInsertion import *



# Create Tables if not exists
create_tables()

key = "AIzaSyDqfPE99DZFTKO2bHaPAswJL7qyoKQQDFE"
# pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Any?levels=administrativeArea1&key=[YOUR_API_KEY]"
pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Any?levels=country&levels=administrativeArea1&key=[YOUR_API_KEY]"
url = pre_url.replace("[YOUR_API_KEY]",key)
# print(url)

response = requests.get(url)
# print(response.text)

data = json.loads(response.text)
# print(data)

offices = data['offices']
officials = data['officials']
divisions = data['divisions']
# print('*'*20+"Offices"+"*"*20)
# print(offices)
# print('*'*20+"officials"+"*"*20)
# print(officials)
# print('*'*20+"divisions"+"*"*20)
# print(divisions)

for office in offices:
    name = office['name']
    divisionId =office['divisionId']
    divison = divisions[divisionId]['name']
    # print(name,' == ', divison)
    if len(office['levels']) > 1:
        levels = ', '.join(office['levels'])
    else:    
        levels = office['levels'][0]
    # print('levels == ',levels) 

    if len(office['roles']) > 1:
        roles = ', '.join(office['roles'])
    else:    
        roles = office['roles'][0]
    # print('roles == ',roles)
    
    values = (name,divison,levels,roles) 
    office_id = data_insert_into_offices(values) 
    print(office_id)

    
