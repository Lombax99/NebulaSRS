import psycopg2
#from flask import Flask, render_template
#import json

cnx = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
#query = ("""SELECT * FROM TEST;""")

def prova():
    '''cnx = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
    query = ("""SELECT * FROM TEST;""")
    #data_list = []
    try:
        with cnx as conn:
            with conn.cursor() as cur:
                #for q in query:
                cur.execute(query)
                machine_data = cur.fetchall()  # Fetch all rows at once
                # Convert data to a JSON-friendly format
                #for row in machine_data:
                    #data_list.append(dict(zip([col.name for col in cur.description], row)))
                
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if cnx:
            cnx.close()
            print("Connessione al database chiusa")

    return machine_data'''
    return "Hello, world!"
    
#test()
  