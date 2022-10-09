import psycopg2
from config import config

def data_insert_into_offices(values):
    """ Data insert into the table offices """
    sql = """INSERT INTO offices(name,division,levels,roles)
             VALUES(%s,%s,%s,%s) RETURNING id;"""

    conn = None

    try:
        # read connection parameters
        params = config() 

        # connect to the PostgreSql Server
        print("Connecting to the PostgreSql Database....")
        conn = psycopg2.connect(**params)

        #Create cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, values)
        # get the generated id back
        office_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')
        return office_id  

