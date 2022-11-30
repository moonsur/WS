import psycopg2
from config import config
import time

def create_tables():
    """ Create Table into database(PostgreSQL) if does not exists """
    commands = ("""
    CREATE TABLE IF NOT EXISTS election(
        id SERIAL NOT NULL PRIMARY KEY,
        state VARCHAR(255) NOT NULL,
        city VARCHAR(255),
        office VARCHAR(255) NOT NULL,
        sub_office VARCHAR(255),        
        election_type VARCHAR(255),
        election_name VARCHAR(500),
        election_date DATE,
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sub_election(
        id SERIAL NOT NULL PRIMARY KEY,
        election_id INT,
        state VARCHAR(255) NOT NULL,
        city VARCHAR(255),
        office VARCHAR(255) NOT NULL,
        sub_office VARCHAR(255),
        election_type VARCHAR(255),
        party VARCHAR(255),
        election_name VARCHAR(255),
        election_date DATE,        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_election FOREIGN KEY(election_id) REFERENCES election(id) ON DELETE CASCADE         
    )
    """,    
     """ 
    CREATE TABLE IF NOT EXISTS candidate(
        id SERIAL NOT NULL PRIMARY KEY,        
        name VARCHAR(400),
        photo_url VARCHAR(2024),
        party VARCHAR(200),
        incumbent VARCHAR(10),
        prior_offices VARCHAR(1024),
        current_office VARCHAR(400),
        profession VARCHAR(200),                
        candidate_url VARCHAR(2024),        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ
    )
    """,    
     """
    CREATE TABLE IF NOT EXISTS education(
        id SERIAL NOT NULL PRIMARY KEY,
        degree VARCHAR(255),
        institute VARCHAR(500),        
        candidate_id INT NOT NULL,
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_candidate FOREIGN KEY(candidate_id) REFERENCES candidate(id) ON DELETE CASCADE
    )
    """,
     """
    CREATE TABLE IF NOT EXISTS contact(
        id SERIAL NOT NULL PRIMARY KEY,
        channel_name VARCHAR(255),
        channel_url VARCHAR(500),        
        candidate_id INT NOT NULL,
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_candidate FOREIGN KEY(candidate_id) REFERENCES candidate(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS election_result(
        id SERIAL NOT NULL PRIMARY KEY,
        candidate_id INT,
        vote_percentage VARCHAR(10),        
        vote_number VARCHAR(10),
        election_id INT,
        sub_election_id INT,
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_candiate FOREIGN KEY(candidate_id) REFERENCES candidate(id) ON DELETE CASCADE,
        CONSTRAINT fk_election FOREIGN KEY(election_id) REFERENCES election(id) ON DELETE CASCADE,
        CONSTRAINT fk_sub_election FOREIGN KEY(sub_election_id) REFERENCES sub_election(id) ON DELETE CASCADE
    )
    """,
    )

    conn = None

    try:
        # read connection parameters
        params = config() 
        # start_time = time.time()
        # connect to the PostgreSql Server        
        conn = psycopg2.connect(**params)
        # print("database connection establishing time --- %s seconds ---" % (time.time() - start_time)) 
        # start_time = time.time() 
        #Create cursor
        cur = conn.cursor()
        # print("database cursor creation time --- %s seconds ---" % (time.time() - start_time))
        for command in commands:
            cur.execute(command)            

        # start_time = time.time()
        # Close communication with PostgreSql Database
        cur.close()
        # print("database connection closing time --- %s seconds ---" % (time.time() - start_time)) 
        # commit the changes
        conn.commit()  

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
                   