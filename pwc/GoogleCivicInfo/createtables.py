import psycopg2
from config import config

def create_tables():
    """ Create Table into database(PostgreSQL) if does not exists """
    commands = ("""
    CREATE TABLE IF NOT EXISTS offices(
        id SERIAL NOT NULL,
        name VARCHAR(255),
        division VARCHAR(255),
        levels VARCHAR(255),
        roles VARCHAR(255),
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,        
        PRIMARY KEY (id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS officials(
        id SERIAL NOT NULL,
        office_id INT,
        name VARCHAR(255),
        party VARCHAR(255),
        phones VARCHAR(255),
        urls VARCHAR(512),
        photoUrl VARCHAR(512),
        emails VARCHAR(512),        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,        
        PRIMARY KEY (id),
        CONSTRAINT fk_office FOREIGN KEY(office_id) REFERENCES offices(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS address(
        id SERIAL NOT NULL,
        official_id INT,
        line1 VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        zip VARCHAR(255),
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,        
        PRIMARY KEY (id),
        CONSTRAINT fk_official FOREIGN KEY(official_id) REFERENCES officials(id)
    )
    """,
     """
    CREATE TABLE IF NOT EXISTS channels(
        id SERIAL NOT NULL,
        official_id INT,
        type VARCHAR(125),
        channel_id VARCHAR(255),        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,        
        PRIMARY KEY (id),
        CONSTRAINT fk_official FOREIGN KEY(official_id) REFERENCES officials(id)
    )
    """,
     """
    CREATE TABLE IF NOT EXISTS geocodingSummaries(
        id SERIAL NOT NULL,
        official_id INT,
        queryString VARCHAR(255),
        cellId VARCHAR(125),        
        fprint VARCHAR(125),        
        featureType VARCHAR(125),        
        positionPrecisionMeters INT,        
        addressUnderstood BOOLEAN,        
        created TIMESTAMPTZ,
        updated TIMESTAMPTZ,        
        PRIMARY KEY (id),
        CONSTRAINT fk_official FOREIGN KEY(official_id) REFERENCES officials(id)
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
                   