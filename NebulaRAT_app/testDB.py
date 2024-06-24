from psycopg import connect

def testQuery():
    conn = connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
    cur = conn.cursor()                
    cur.execute("SELECT * FROM TEST;")
    machine_data = cur.fetchall()
    conn.commit() 
    cur.close()
    conn.close()
    return machine_data