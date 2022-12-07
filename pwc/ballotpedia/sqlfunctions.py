import psycopg2
from datetime import datetime, timezone
import logging
import sys


def get_election_id(conn, state_name, office, sub_office, election_type, election_date, election_name):
    try:
        cur = conn.cursor()
        election_id = 0

        if election_date == '':
            sql = f"""SELECT id FROM election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and election_name=%s""" 
            values = (state_name, office, sub_office, election_type, election_name)
        else:
            sql = f"""SELECT id FROM election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and election_date=%s and election_name=%s""" 
            values = (state_name, office, sub_office, election_type, election_date, election_name)    

        cur.execute(sql,values)
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
        conn.rollback()
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
        conn.rollback()
        print(error)
        logging.error(f"Function: insert_into_election. Error: {error}")    


def get_sub_election_id(conn, state_name, office, sub_office, election_type, party,  sub_election_date, election_name):
    print(f"get_sub_election_id==> state_name={state_name}, office={office}, sub_office={sub_office}, election_type={election_type}, party={party},  sub_election_date={sub_election_date} election_name={election_name}")
    logging.info(f"get_sub_election_id==> state_name={state_name}, office={office}, sub_office={sub_office}, election_type={election_type}, party={party},  sub_election_date={sub_election_date} election_name={election_name}")
    try:
        cur = conn.cursor()
        sub_election_id = 0
        general_election_id = 0
        if sub_election_date == '':
            sql = f"""SELECT id, election_id FROM sub_election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and party=%s and election_name=%s""" 
            values = (state_name, office, sub_office, election_type, party, election_name)
            cur.execute(sql,values)
        else:    
            sql = f"""SELECT id, election_id FROM sub_election WHERE state=%s and office=%s and sub_office=%s and election_type=%s and party=%s and election_date=%s and election_name=%s""" 
            values = (state_name, office, sub_office, election_type, party, sub_election_date, election_name)
            cur.execute(sql,values)

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
        conn.rollback()
        print(error)
        logging.error(f"Function: get_sub_election_id. Error: {error}")


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
        conn.rollback()
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
        conn.rollback()        
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
        conn.rollback()       
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
        conn.rollback()
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
        conn.rollback()
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
        conn.rollback()     
        print(error)
        logging.error(f"Function: update_candidate. Error: {error}") 
        return False

def get_election_result_id(conn, candidate_id, general_election_id, sub_election_id, election_type):
    try:
        cur = conn.cursor()
        election_result_id = 0
        if 'general' in election_type:
            sql = f"""SELECT id FROM election_result WHERE candidate_id=%s and election_id=%s;""" 
            values = (candidate_id,general_election_id)
        else:
            sql = f"""SELECT id FROM election_result WHERE candidate_id=%s and sub_election_id=%s;""" 
            values = (candidate_id, sub_election_id)

        cur.execute(sql,values)
        fetch_val = cur.fetchone()
        if fetch_val is not None:
            election_result_id = fetch_val[0]  
        cur.close()
        return election_result_id
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()       
        print(error)
        logging.error(f"Function: get_election_result_id. Error: {error}") 
        

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
        conn.rollback()      
        print(error)
        logging.error(f"Function: insert_into_election_result. Error: {error}") 
        return False    



def update_election_result(conn, vote_percentage, vote_number, election_result_id):
    try:
        cur = conn.cursor()
        now = str(datetime.now(timezone.utc))
        sql = """UPDATE election_result SET vote_percentage = %s, vote_number = %s, updated = %s WHERE id = %s;"""
        values = (vote_percentage, vote_number, now, election_result_id)         
        cur.execute(sql, values)
         
        # commit the changes to the database
        conn.commit()
        cur.close()
        logging.info(f"&&&=> Election result update succesfully with id = {election_result_id}")
        return True
    except (Exception, psycopg2.DatabaseError) as error: 
        conn.rollback()       
        print(error)
        logging.error(f"Function: update_election_result. Error: {error}") 
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
        conn.rollback()      
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
        conn.rollback()       
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
        conn.rollback()    
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
        conn.rollback()       
        print(error)
        logging.error(f"Function: insert_into_contact. Error: {error}")     
    



  ###################################################################################

