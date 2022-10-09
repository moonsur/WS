import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE IF NOT EXISTS offices (
            id integer NOT NULL,
            name VARCHAR(255) NOT NULL,
            divisionId VARCHAR(100),
            levels VARCHAR(100),
            roles VARCHAR(100),
            officialIndices VARCHAR(25),
            PRIMARY KEY (id)
        )
        """,)
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        for command in commands:
            if cur.execute(command):
                print("Table created successfully!")
            else:
                print("Table not created!")    
        # cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')    