import psycopg2
from datetime import datetime, timezone

def data_insert_into_offices(conn,cur,values):
    """ Data insert into the table offices """
    sql = """INSERT INTO offices(name,division,levels,roles,created)
             VALUES(%s,%s,%s,%s,%s) RETURNING id;"""

    select_sql = f"""SELECT id FROM offices WHERE name='{values[0]}' and division='{values[1]}' and levels='{values[2]}' and roles='{values[3]}'""" 
            
    
    office_id = None
    try:
        id = None
        cur.execute(select_sql)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            id = fetch_val[0] 
            res = (0,id)
            # update_sql = f"""UPDATE TABLE offices set division='{values[1]} WHERE id='{id}'"""
            
        print("id== ",id)

        if id is None: 
            print("start inserting...")    
            cur.execute(sql, values)
            # get the generated id back
            office_id = cur.fetchone()[0]
            res = (1,office_id)
            # commit the changes to the database
            conn.commit()
        # else:
        #     office_id = id

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
    party = official_details['party']
    phones = ', '.join(official_details['phones'])
    urls = ', '.join(official_details['urls'])
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
        id = None 

        print("start inserting...")    
        cur.execute(sql, values)
        # get the generated id back
        official_id = cur.fetchone()[0]        
        # commit the changes to the database
        conn.commit()
        print('official_id = > ',official_id)
        """ Insert into address """
        sql_address =  """INSERT INTO address(official_id,line1,city,state,zip,created)
             VALUES(%s,%s,%s,%s,%s,%s);"""
        for address in  official_details['address']:
            line1 = address['line1']
            city = address['city']
            state = address['state']
            zip_code = address['zip']
            address_created = str(datetime.now(timezone.utc)) 
            address_values = (official_id, line1, city, state, zip_code, address_created)
            cur.execute(sql_address, address_values)
            conn.commit()

        """ Insert into channels """  
        sql_channel =  """INSERT INTO channels(official_id,type,channel_id,created)
             VALUES(%s,%s,%s,%s);"""
        for channel in official_details['channels']: 
            channel_type =  channel['type']
            channel_id = channel['id']
            channel_created = str(datetime.now(timezone.utc)) 
            channel_values = (official_id, channel_type, channel_id, channel_created)
            cur.execute(sql_channel, channel_values)
            conn.commit()

        """ Insert into geocodingSummaries """ 
        sql_geocoding =  """INSERT INTO geocodingSummaries(official_id,queryString,cellId,fprint,featureType,positionPrecisionMeters,addressUnderstood,created)
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s);"""
        for geocodingSummary in official_details['geocodingSummaries']:
            queryString = geocodingSummary['queryString']
            cellId = geocodingSummary['featureId']['cellId']
            fprint = geocodingSummary['featureId']['fprint']
            featureType = geocodingSummary['featureType']
            positionPrecisionMeters = geocodingSummary['positionPrecisionMeters']
            addressUnderstood = geocodingSummary['addressUnderstood']
            geocoding_created = str(datetime.now(timezone.utc)) 
            geocoding_values = (official_id, queryString, cellId, fprint, featureType, positionPrecisionMeters, addressUnderstood, geocoding_created)
            cur.execute(sql_geocoding,  geocoding_values)
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None         
