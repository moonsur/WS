import time
import requests
import json
from createtables import create_tables
from insertUpdate import *
import psycopg2
from config import config
from datetime import datetime, timezone
import os

http_urls_file_dir = os.path.dirname(os.path.abspath(__file__))
http_urls_file_path = http_urls_file_dir + '\\http-for-states.txt'
# read connection parameters
params = config() 
print(params)
# Create Tables if not exists
create_tables()

key = "AIzaSyDqfPE99DZFTKO2bHaPAswJL7qyoKQQDFE"

with open(http_urls_file_path, 'r') as f:
    lines = f.readlines()
    cont = 0
    for line in lines:
        cont += 1
        print('State no = ',cont)       
        if cont == 35:
            print('Wait for 10 seconds...')
            time.sleep(10)
        pre_url = line.strip()        
        url = pre_url.replace("[YOUR_API_KEY]",key)
        print(url)

        response = requests.get(url)
        print(response.text)
        # break
        data = json.loads(response.text)
        # print(data)

        offices = data['offices']
        officials = data['officials']
        divisions = data['divisions']

        conn = None
        cur = None
        try:           
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
                
                if len(office['levels']) > 1:
                    levels = ', '.join(office['levels'])
                else:    
                    levels = office['levels'][0]                 

                if len(office['roles']) > 1:
                    roles = ', '.join(office['roles'])
                else:    
                    roles = office['roles'][0]                
            
                values = (name,divison,levels,roles,str(datetime.now(timezone.utc)))  
                res = data_insert_into_offices(conn, cur, values) 
                print(res)
                if res[0] == 0:
                    for officialind in office['officialIndices']:                        
                        official_details = officials[officialind]                        
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
    
