import urllib.parse
import os

def get_connetion_uri():
    dbhost = 'nebularat-postgresdb-server.postgres.database.azure.com'
    dbname = 'nebularat-postgresServer-db'
    dbuser = 'sudo'
    password = 'sudo'
    sslmode = 'require'

    db_uri = f"postgresql://{dbuser}:{password}@{dbhost}/{dbname}?sslmode={sslmode}"

    return db_uri

def prova():
    import psycopg2
    try:
        conn_string = get_connetion_uri()
        with psycopg2.connect(**conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM TEST;")
                data = cursor.fetchall()
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
        
    return data

if __name__ == '__main__':
   prova()