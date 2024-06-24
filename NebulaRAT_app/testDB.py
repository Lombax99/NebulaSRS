import urllib.parse
import os

def prova():
    import psycopg2
    try:
        with psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="postgres") as conn:
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