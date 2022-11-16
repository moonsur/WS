import psycopg2
from datetime import datetime, timezone

def data_insert_into_offices(conn,cur,values):
    """ Data insert into the table offices """
    sql = """INSERT INTO offices(name,division,levels,roles,created)
             VALUES(%s,%s,%s,%s,%s) RETURNING id;"""
    
    select_sql = f"""SELECT id FROM offices WHERE name=%s and division=%s and levels=%s and roles=%s""" 
    select_values = (values[0],values[1],values[2],values[3])            
    
    office_id = None
    try:
        id = None
        cur.execute(select_sql,select_values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            id = fetch_val[0] 
            res = (0,id)
                       
        # print("id== ",id)

        if id is None: 
            # print("start inserting...")    
            cur.execute(sql, values)
            # get the generated id back
            office_id = cur.fetchone()[0]
            res = (1,office_id)
            # commit the changes to the database
            conn.commit()        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:       
        return res

def insert_into_officials(conn,cur, official_details, office_id):
    """ Insert officials informaion into table. """
    sql = """INSERT INTO officials(office_id,name,party,phones,urls,photoUrl,emails,created)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""

    name = official_details['name']
    if 'party' in official_details:
        party = official_details['party']
    else:
        party = '' 
    if 'phones' in official_details:       
        phones = ', '.join(official_details['phones'])
    else:
         phones = '' 
    if 'urls' in official_details:       
        urls = ', '.join(official_details['urls'])
    else:
        urls = ''    
    if 'photoUrl' in official_details:
        photoUrl = official_details['photoUrl']
    else:
         photoUrl = '' 
    if 'emails' in official_details:
        emails = ', '.join(official_details['emails'])
    else:
         emails = '' 
    official_created = str(datetime.now(timezone.utc))  

    values = (office_id, name, party, phones, urls, photoUrl, emails, official_created)
    official_id = None
    try:
        # print("start inserting...")    
        cur.execute(sql, values)
        # get the generated id back
        official_id = cur.fetchone()[0]        
        # commit the changes to the database
        conn.commit()
        print('official_id = > ',official_id)

        """ Insert into address """
        sql_address =  """INSERT INTO address(official_id,line1,city,state,zip,created)
             VALUES(%s,%s,%s,%s,%s,%s);"""
        if 'address' in official_details:     
            for address in  official_details['address']:
                if 'line1' in address: 
                    line1 = address['line1']
                else:
                    line1 = ''    
                if 'city' in address: 
                    city = address['city']
                else:
                    city = ''    
                if 'state' in address: 
                    state = address['state']
                else:
                    state = ''    
                if 'zip' in address: 
                    zip_code = address['zip']
                else:
                    zip_code = ''   
                
                date_now = str(datetime.now(timezone.utc)) 
                address_values = (official_id, line1, city, state, zip_code, date_now)
                cur.execute(sql_address, address_values)
                conn.commit()

        """ Insert into channels """  
        sql_channel =  """INSERT INTO channels(official_id,type,channel_id,created)
             VALUES(%s,%s,%s,%s);"""
        if 'channels' in official_details:     
            for channel in official_details['channels']:
                if 'type' in channel: 
                    channel_type =  channel['type']
                else:
                    channel_type = '' 
                if 'id' in channel:       
                    channel_id = channel['id']
                else:
                     channel_id = ''   
                date_now = str(datetime.now(timezone.utc)) 
                channel_values = (official_id, channel_type, channel_id, date_now)
                cur.execute(sql_channel, channel_values)
                conn.commit()

        """ Insert into geocodingSummaries """ 
        sql_geocoding =  """INSERT INTO geocodingSummaries(official_id,queryString,cellId,fprint,featureType,positionPrecisionMeters,addressUnderstood,created)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
        if 'geocodingSummaries' in official_details:     
            for geocodingSummary in official_details['geocodingSummaries']:
                if 'queryString' in geocodingSummary:  
                    queryString = geocodingSummary['queryString']
                else:
                    queryString = '' 
                if 'featureId' in geocodingSummary:
                    if 'cellId' in geocodingSummary['featureId']:        
                        cellId = geocodingSummary['featureId']['cellId']
                    else:
                        cellId = ''   
                    if 'fprint' in geocodingSummary['featureId']:
                        fprint = geocodingSummary['featureId']['fprint']
                    else:
                        fprint = '' 
                if 'featureType' in geocodingSummary:           
                    featureType = geocodingSummary['featureType']
                else:
                    featureType = '' 
                if 'positionPrecisionMeters' in geocodingSummary:      
                    positionPrecisionMeters = geocodingSummary['positionPrecisionMeters']
                else:
                    positionPrecisionMeters = ''  
                if 'addressUnderstood' in geocodingSummary:      
                    addressUnderstood = geocodingSummary['addressUnderstood']
                else:
                    addressUnderstood = ''    
                date_now = str(datetime.now(timezone.utc)) 
                geocoding_values = (official_id, queryString, cellId, fprint, featureType, positionPrecisionMeters, addressUnderstood, date_now)
                cur.execute(sql_geocoding,  geocoding_values)
                conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None 


def update_officials(conn,cur, official_details, office_id):     
    select_official_sql = f"""SELECT id FROM officials WHERE office_id=%s and name=%s and party=%s"""     
    if 'name' in official_details:
        offical_name = official_details['name']
    else:
         offical_name = ''   
    if 'party' in official_details:
        offical_party = official_details['party']
    else:
         offical_party = ''   
    select_official_values = (office_id,offical_name,offical_party)
    official_id = None  
    try:
        cur.execute(select_official_sql,select_official_values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            official_id = fetch_val[0] 
                   
        name = official_details['name']
        if 'party' in official_details:
            party = official_details['party']
        else:
            party = '' 
        if 'phones' in official_details:       
            phones = ', '.join(official_details['phones'])
        else:
            phones = '' 
        if 'urls' in official_details:       
            urls = ', '.join(official_details['urls'])
        else:
            urls = ''        
        if 'photoUrl' in official_details:
            photoUrl = official_details['photoUrl']
        else:
            photoUrl = '' 
        if 'emails' in official_details:
            emails = ', '.join(official_details['emails'])
        else:
            emails = '' 
        date_now = str(datetime.now(timezone.utc))

        if official_id is not None:
            # print("official id is not none.. update")
            official_update_sql = """UPDATE officials set phones=%s,urls=%s,photoUrl=%s,emails=%s,updated=%s WHERE id=%s""" 
            official_update_values = (phones,urls,photoUrl,emails,date_now,official_id)  
            cur.execute(official_update_sql, official_update_values)
            # commit the changes to the database
            conn.commit()
        else:
            # print("official id is  none.. insert")
            official_insert_sql = """INSERT INTO officials(office_id,name,party,phones,urls,photoUrl,emails,created)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
            official_insert_values = (office_id, name, party, phones, urls, photoUrl, emails, date_now)
            cur.execute(official_insert_sql, official_insert_values)
            # get the generated id back
            official_id = cur.fetchone()[0]        
            # commit the changes to the database
            conn.commit()
           

        """ update into address """
        address_id = None
        if 'address' in official_details: 
            for address in  official_details['address']:
                if 'line1' in address: 
                    line1 = address['line1']
                else:
                    line1 = ''    
                if 'city' in address: 
                    city = address['city']
                else:
                    city = ''    
                if 'state' in address: 
                    state = address['state']
                else:
                    state = ''    
                if 'zip' in address: 
                    zip_code = address['zip']
                else:
                    zip_code = '' 

                date_now = str(datetime.now(timezone.utc)) 

                select_address_sql = f"""SELECT id FROM address WHERE official_id='{official_id}' """ 
                cur.execute(select_address_sql)
                fetch_val = cur.fetchone()
                if fetch_val is not None:
                    address_id = fetch_val[0]
                if address_id is not None:
                    # print("address id is not none.. update")
                    address_update_sql = f"""UPDATE address set line1=%s,city=%s,state=%s,zip=%s,updated=%s WHERE id=%s"""                 
                    address_update_values = (line1, city, state, zip_code, date_now,address_id)  
                    cur.execute(address_update_sql, address_update_values)
                    # commit the changes to the database
                    conn.commit()
                else:   
                    # print("address id is  none.. insert")         
                    sql_insert_address =  """INSERT INTO address(official_id,line1,city,state,zip,created)
                VALUES(%s,%s,%s,%s,%s,%s);"""
                    address_values = (official_id, line1, city, state, zip_code, date_now)
                    cur.execute(sql_insert_address, address_values)
                    conn.commit()

        """ Update into channels """  
        
        if 'channels' in official_details:     
            for channel in official_details['channels']:
                if 'type' in channel: 
                    channel_type =  channel['type']
                else:
                    channel_type = '' 
                if 'id' in channel:       
                    ch_id = channel['id']
                else:
                     ch_id = ''   
                date_now = str(datetime.now(timezone.utc)) 
                
                channel_id = None
                select_channel_sql = f"""SELECT id FROM channels WHERE official_id='{official_id}' and type='{channel_type}' """ 
                cur.execute(select_channel_sql)
                fetch_val = cur.fetchone()
                if fetch_val is not None:
                    channel_id = fetch_val[0]

                if channel_id is not None:
                    # print("channel id is not none.. update")
                    channel_update_sql = f"""UPDATE channels set channel_id=%s, updated=%s WHERE id=%s"""                 
                    channel_update_values = (ch_id, date_now,channel_id)  
                    cur.execute(channel_update_sql, channel_update_values)
                    # commit the changes to the database
                    conn.commit()
                else:   
                    # print("channel id is  none.. insert")         
                    sql_insert_channel =  """INSERT INTO channels(official_id,type,channel_id,created)
             VALUES(%s,%s,%s,%s);"""

                    channel_insert_values = (official_id, channel_type, channel_id, date_now)
                    cur.execute(sql_insert_channel, channel_insert_values)
                    conn.commit()

        """ Update geocodingSummaries """ 
        
        if 'geocodingSummaries' in official_details:     
            for geocodingSummary in official_details['geocodingSummaries']:
                if 'queryString' in geocodingSummary:  
                    queryString = geocodingSummary['queryString']
                else:
                    queryString = '' 
                if 'featureId' in geocodingSummary:
                    if 'cellId' in geocodingSummary['featureId']:        
                        cellId = geocodingSummary['featureId']['cellId']
                    else:
                        cellId = ''   
                    if 'fprint' in geocodingSummary['featureId']:
                        fprint = geocodingSummary['featureId']['fprint']
                    else:
                        fprint = '' 
                if 'featureType' in geocodingSummary:           
                    featureType = geocodingSummary['featureType']
                else:
                    featureType = '' 
                if 'positionPrecisionMeters' in geocodingSummary:      
                    positionPrecisionMeters = geocodingSummary['positionPrecisionMeters']
                else:
                    positionPrecisionMeters = ''  
                if 'addressUnderstood' in geocodingSummary:      
                    addressUnderstood = geocodingSummary['addressUnderstood']
                else:
                    addressUnderstood = ''    
                date_now = str(datetime.now(timezone.utc))

                geocoding_id = None
                select_geocoding_sql = f"""SELECT id FROM geocodingSummaries WHERE official_id='{official_id}'""" 
                cur.execute(select_geocoding_sql)
                fetch_val = cur.fetchone()
                if fetch_val is not None:
                    geocoding_id = fetch_val[0]

                if geocoding_id is not None:
                    # print("geocoding id is not none.. update")
                    geocoding_update_sql = f"""UPDATE geocodingSummaries set queryString=%s,cellId=%s,fprint=%s,featureType=%s,positionPrecisionMeters=%s,addressUnderstood=%s, updated=%s WHERE id=%s"""                 
                    geocoding_update_values = (queryString, cellId, fprint, featureType, positionPrecisionMeters, addressUnderstood, date_now,geocoding_id)  
                    cur.execute(geocoding_update_sql, geocoding_update_values)
                    # commit the changes to the database
                    conn.commit()
                else:   
                    # print("geocoding id is  none.. insert")         
                    sql_geocoding_insert =  """INSERT INTO geocodingSummaries(official_id,queryString,cellId,fprint,featureType,positionPrecisionMeters,addressUnderstood,created)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""

                    geocoding_values_update = (official_id, queryString, cellId, fprint, featureType, positionPrecisionMeters, addressUnderstood, date_now)
                    cur.execute(sql_geocoding_insert,  geocoding_values_update)
                    conn.commit()            
                

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
