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
        PRIMARY KEY (id)
    )
    """,)

    conn = None

    try:
        # read connection parameters
        params = config() 

        # connect to the PostgreSql Server
        print("Connecting to the PostgreSql Database....")
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
            print('Database connection closed')        