import psycopg2
from datetime import datetime, timezone
import logging
import sys


def get_election_id(conn, state_name, office, sub_office, election_type, election_date):
    try:
        cur = conn.cursor()
        election_id = 0
        select_sql = f"""SELECT id FROM election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and election_date=%s""" 
        select_values = (state_name, office, sub_office, election_type, election_date)
        cur.execute(select_sql,select_values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            election_id = fetch_val[0]  
        cur.close()
        if election_id == 0:
            logging.info(f"=======> Election not found")
        else:
            logging.info(f"=======> Election found, id = {election_id}")    
        return election_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: get_election_id. Error: {error}") 

def insert_into_election(conn, state_name, office, sub_office, election_type, election_name, election_date, city=''):
    logging.info(f"Function: insert_into_election, values:[state_name:{state_name}, office:{office}, sub_office:{sub_office}, election_type:{election_type}, election_name:{election_name}, election_date:{election_date}, city:{city}]")
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        sql = """INSERT INTO election(state, city, office, sub_office, election_type, election_name, election_date, created)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
        values = (state_name, city, office, sub_office, election_type, election_name, election_date, now)         
        cur.execute(sql, values)
        # get the generated id back
        general_election_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
        return general_election_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: insert_into_election. Error: {error}")    


def get_sub_election_id(conn, state_name, office, sub_office, election_type, party,  primary_runoff_election_date):
    try:
        cur = conn.cursor()
        sub_election_id = 0
        general_election_id = 0
        
        select_sql = f"""SELECT id, election_id FROM sub_election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and party=%s and election_date=%s""" 
        select_values = (state_name, office, sub_office, election_type, party, primary_runoff_election_date)
        cur.execute(select_sql,select_values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            sub_election_id = fetch_val[0]
            if fetch_val[1] is not None:
                general_election_id = fetch_val[1]   
        cur.close()
        if sub_election_id == 0:
            logging.info(f"=======> Sub Election not found")
        else:
            logging.info(f"=======> Sub Election found, id = {sub_election_id}")    
        return (sub_election_id,general_election_id)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: get_election_id. Error: {error}")


def insert_into_sub_election(conn, general_election_id, state_name, office, sub_office, election_type, party, election_name, election_date, city=''):
    logging.info(f"Function: insert_into_sub_election, values:[general_election_id:{general_election_id}, state_name:{state_name}, office:{office}, sub_office:{sub_office}, election_type:{election_type}, election_name:{election_name}, election_date:{election_date}, city:{city}]")
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        if general_election_id != 0:
            if election_date == '':
                sql = """INSERT INTO sub_election(election_id, state, city, office, sub_office, election_type, party, election_name, created)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
                values = (general_election_id, state_name, city, office, sub_office, election_type, party, election_name, now)
            else:    
                sql = """INSERT INTO sub_election(election_id, state, city, office, sub_office, election_type, party, election_name, election_date, created)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
                values = (general_election_id, state_name, city, office, sub_office, election_type, party, election_name, election_date, now)
        else:
            if election_date == '':
                sql = """INSERT INTO sub_election(state, city, office, sub_office, election_type, party, election_name, created)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
                values = (state_name, city, office, sub_office, election_type, party, election_name, now)
            else:    
                sql = """INSERT INTO sub_election(state, city, office, sub_office, election_type, party, election_name, election_date, created)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
                values = (state_name, city, office, sub_office, election_type, party, election_name, election_date, now)  

        cur.execute(sql, values)
        # get the generated id back
        sub_election_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
        return sub_election_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: insert_into_sub_election. Error: {error}")     


def update_sub_election(conn, sub_election_id, general_election_id):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        #sub_election(election_id
        sql = """UPDATE sub_election SET election_id = %s, updated = %s WHERE id = %s;"""
        values = (general_election_id,now, sub_election_id)         
        cur.execute(sql, values)
         
        # commit the changes to the database
        conn.commit()
        cur.close()
        logging.info(f"&&&=> Sub Election update succesfully with id = {sub_election_id}, general id = {general_election_id}")
        return True
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: update_sub_election. Error: {error}") 
        return False


def get_candidate_id(conn, candidate_url):
    try:
        cur = conn.cursor()
        candidate_id = 0
        select_sql = f"""SELECT id FROM candidate WHERE candidate_url=%s""" 
        select_values = (candidate_url,)
        cur.execute(select_sql,select_values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            candidate_id = fetch_val[0]  
        cur.close()
        return candidate_id
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: get_candidate_id. Error: {error}") 
            

def get_all_candidate_url(conn):
    try:
        cur = conn.cursor()    
        select_sql = f"""SELECT id, candidate_url FROM candidate""" 
        
        cur.execute(select_sql)
        fetch_values = cur.fetchall()
        print('query-- len: ', len(fetch_values))
        # print(fetch_values)
        ret_dict = {row[1]: row[0] for row in fetch_values} 
        cur.close()
        return ret_dict 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: get_all_candidate_url. Error: {error}")   


def insert_into_candidate(conn, name, photo_url, party, incumbent, prior_offices, current_office, profession, candidate_url):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        sql = """INSERT INTO candidate(name, photo_url, party, incumbent, prior_offices, current_office, profession, candidate_url,created)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""
        values = (name, photo_url, party, incumbent, prior_offices, current_office, profession, candidate_url, now)         
        cur.execute(sql, values)
        # get the generated id back
        candidate_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
        return candidate_id
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        logging.error(f"Function: insert_into_candidate. Error: {error}")    


def update_candidate(conn, photo_url, party, incumbent, prior_offices, current_office, profession, candidate_id):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        sql = """UPDATE candidate SET photo_url = %s, party = %s, incumbent = %s, prior_offices = %s, current_office = %s, profession = %s, updated = %s
                WHERE id = %s;"""
        values = (photo_url, party, incumbent, prior_offices, current_office, profession, now, candidate_id)         
        cur.execute(sql, values)
         
        # commit the changes to the database
        conn.commit()
        cur.close()
        logging.info(f"&&&=> Candidate update succesfully with id = {candidate_id}")
        return True
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: update_candidate. Error: {error}") 
        return False

def insert_into_election_result(conn, candidate_id, vote_percentage, vote_number, general_election_id, sub_election_id, election_type):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        if 'general' in election_type:
            sql = """INSERT INTO election_result(candidate_id, vote_percentage, vote_number, election_id, created)
                    VALUES(%s,%s,%s,%s,%s) RETURNING id;"""
            values = (candidate_id, vote_percentage, vote_number, general_election_id, now)
        else:
            sql = """INSERT INTO election_result(candidate_id, vote_percentage, vote_number, sub_election_id, created)
                    VALUES(%s,%s,%s,%s,%s) RETURNING id;"""
            values = (candidate_id, vote_percentage, vote_number, sub_election_id, now)           
        cur.execute(sql, values)
        # get the generated id back
        election_result_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: insert_into_election_result. Error: {error}") 
        return False    


def get_educations_by_candidate_id(conn, candidate_id):
    try:
        cur = conn.cursor()
        
        sql ="""SELECT degree, institute FROM education WHERE candidate_id = %s"""
        values = (candidate_id,)
        cur.execute(sql,values)
        edu_info = cur.fetchall()
        
        cur.close()
        return edu_info
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: get_educations_by_candidate_id. Error: {error}") 
        return False 


def insert_into_education(conn, degree, institute, candidate_id):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        
        sql = """INSERT INTO education(degree, institute, candidate_id, created)
                VALUES(%s,%s,%s,%s) RETURNING id;"""
        values = (degree, institute, candidate_id, now)                
        cur.execute(sql, values)
        # get the generated id back
        education_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: insert_into_education. Error: {error}") 
            

def get_contacts_by_candidate_id(conn, candidate_id):
    try:
        cur = conn.cursor()
        
        sql ="""SELECT channel_name, channel_url FROM contact WHERE candidate_id = %s"""
        values = (candidate_id,)
        cur.execute(sql,values)
        con_info = cur.fetchall()
        cur.close()
        return con_info
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: get_contacts_by_candidate_id. Error: {error}") 
        return False 

def insert_into_contact(conn, channel_name, channel_url, candidate_id):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        
        sql = """INSERT INTO contact(channel_name, channel_url, candidate_id, created)
                VALUES(%s,%s,%s,%s) RETURNING id;"""
        values = (channel_name, channel_url, candidate_id, now)
                
        cur.execute(sql, values)
        # get the generated id back
        contact_id = cur.fetchone()[0]    
        # commit the changes to the database
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:        
        print(error)
        logging.error(f"Function: insert_into_contact. Error: {error}")     
    



  ###################################################################################


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
