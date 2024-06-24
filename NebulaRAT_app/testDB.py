import urllib.parse
import os

def prova():
    import psycopg2
    try:
        with psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM TEST;")
                machine_data = cur.fetchall()
                
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'null'
    finally:
        cur.close()
        conn.close()
        return machine_data
    

if __name__ == '__main__':
    prova()