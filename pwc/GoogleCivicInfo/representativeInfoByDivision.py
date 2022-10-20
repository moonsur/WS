import requests
import json
from createtables import create_tables
from insertUpdate import *
import psycopg2
from config import config
from datetime import datetime, timezone


# Create Tables if not exists
create_tables()

key = "AIzaSyDqfPE99DZFTKO2bHaPAswJL7qyoKQQDFE"
# pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Aak?levels=administrativeArea1&levels=country&key=[YOUR_API_KEY]"
pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Any?levels=administrativeArea1&key=[YOUR_API_KEY]"
# pre_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives/ocd-division%2Fcountry%3Aus%2Fstate%3Any?levels=country&levels=administrativeArea1&key=[YOUR_API_KEY]"
url = pre_url.replace("[YOUR_API_KEY]",key)
# print(url)

response = requests.get(url)
print(response.text)

data = json.loads(response.text)
# print(data)

offices = data['offices']
officials = data['officials']
divisions = data['divisions']

conn = None
cur = None
try:
    # read connection parameters
    params = config() 
    # connect to the PostgreSql Server     
    conn = psycopg2.connect(**params)
    #Create cursor
    cur = conn.cursor()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
        
if conn is not None:
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
       
        values = (name,divison,levels,roles,str(datetime.now(timezone.utc)))  
        res = data_insert_into_offices(conn, cur, values) 
        print(res)
        if res[0] == 0:
            for officialind in office['officialIndices']:
                print('officialind =>',officialind) 
                official_details = officials[officialind]
                # print('official_details ==> ',official_details)
                update_officials(conn,cur, official_details, res[1])
        elif res[0] == 1:
            for officialind in office['officialIndices']:
                official_details = officials[officialind] 
                insert_into_officials(conn,cur, official_details, res[1])

else:
    print("Database connect is not established!")

if cur is not None:
    cur.close()
    print("Cursor closed.")
if conn is not None:    
    conn.close() 
    print("Connection closed.")   
    
