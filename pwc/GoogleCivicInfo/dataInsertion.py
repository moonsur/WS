import psycopg2

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
            update_sql = f"""UPDATE TABLE offices set division='{values[1]} WHERE id='{id}'"""
            
        print("id== ",id)

        if id is None: 
            print("start inserting...")    
            cur.execute(sql, values)
            # get the generated id back
            office_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
        else:
            office_id = id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:       
        return office_id