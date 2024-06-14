import psycopg2
cnx = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
query = (#"""
#INSERT INTO TEST (descrizione)
#VALUES ('pislelo');
#""",
"""
SELECT * FROM TEST;
""")

def test():
    try:
        with cnx as conn:
            with conn.cursor() as cur:
                #for q in query:
                cur.execute(q)
                machine_data = cur.fetchall()  # Fetch all rows at once
                # Convert data to a JSON-friendly format
                data_list = []
                for row in machine_data:
                    data_list.append(dict(zip([col.name for col in cur.description], row)))

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if cnx:
            cnx.close()
            print("Connessione al database chiusa")
    return json.dumps(data_list)

if __name__ == '__main__':
    test()