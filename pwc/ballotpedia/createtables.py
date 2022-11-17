import psycopg2
from config import config

def create_tables():
    """ Create Table into database(PostgreSQL) if does not exists """
    commands = ("""
    CREATE TABLE IF NOT EXISTS election(
        id SERIAL NOT NULL PRIMARY KEY,
        state VARCHAR(255) NOT NULL,
        office VARCHAR(255) NOT NULL,
        sub_office VARCHAR(255),
        election_type VARCHAR(255),
        election_name VARCHAR(500),
        election_date TIMESTAMPTZ,
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sub_election(
        id SERIAL NOT NULL PRIMARY KEY,
        election_id INT NOT NULL,
        election_type VARCHAR(255),
        party VARCHAR(255),
        election_name VARCHAR(255),        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_election FOREIGN KEY(election_id) REFERENCES election(id) ON DELETE CASCADE         
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS election_result(
        id SERIAL NOT NULL PRIMARY KEY,
        vote_percentage DECIMAL(5,2),
        vote_number INT,
        election_id INT,
        sub_election_id INT,
        state VARCHAR(255),
        zip VARCHAR(255),
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,
        CONSTRAINT fk_election FOREIGN KEY(election_id) REFERENCES election(id) ON DELETE CASCADE,
        CONSTRAINT fk_sub_election FOREIGN KEY(sub_election_id) REFERENCES sub_election(id) ON DELETE CASCADE
    )
    """,
     """
    CREATE TABLE IF NOT EXISTS candidate(
        id SERIAL NOT NULL PRIMARY KEY,        
        name VARCHAR(400),
        party VARCHAR(200),
        incumbent VARCHAR(10),
        current_office VARCHAR(400),
        profession VARCHAR(200),
        photo_url VARCHAR(2024),        
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
    CREATE TABLE IF NOT EXISTS result_candidate_junction(
        id SERIAL NOT NULL PRIMARY KEY,                
        candidate_id INT NOT NULL,
        result_id INT NOT NULL,
        CONSTRAINT fk_candidate FOREIGN KEY(candidate_id) REFERENCES candidate(id) ON DELETE CASCADE,
        CONSTRAINT fk_result FOREIGN KEY(result_id) REFERENCES election_result(id) ON DELETE CASCADE
    )
    """,)

    conn = None

    try:
        # read connection parameters
        params = config() 

        # connect to the PostgreSql Server        
        conn = psycopg2.connect(**params)

        #Create cursor
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)            

        # Close communication with PostgreSql Database
        cur.close()
        # commit the changes
        conn.commit()  

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
                   