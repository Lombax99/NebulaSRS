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
    conn_string = get_connetion_uri()
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TEST;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

if __name__ == '__main__':
   prova()