import quickemailverification








def spf2(domain):
    import spf
    try:
        a = spf.check2("192.92.97.241", domain, 'mx.google.com')
        print(a)
    except:
        return "SPF record does not exist"

spf = spf2("franck@ropersevolution.com")
print(spf)

# Table postgre à mettre à jour avec date + nom du fichier + résultat

def insert_database(filename, result):
    import psycopg2
    from datetime import date
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="test",
                                        port="5432",
                                        database="postgres")
        cursor = connection.cursor()
        # Recupère la date du jour

        today = date.today()
        sql = "INSERT INTO table (date, filename, result) VALUES (%s, %s, %s)"
        val = (date, filename, result)
        cursor.execute(sql, val)
        connection.commit()
        print("Record inserted successfully into table")
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS table (
            date DATE,
            filename VARCHAR(255) NOT NULL,
            result VARCHAR(255) NOT NULL
        )
        """)
    conn = None
    try:
        # read the connection parameters
        # connect to the PostgreSQL server
        conn = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="test",
                                        port="5432",
                                        database="postgres")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("Table created successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)
    finally:
        if conn is not None:
            conn.close()







