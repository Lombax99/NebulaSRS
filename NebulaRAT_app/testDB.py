import psycopg2

def testQuery():    
    import psycopg2
    conn = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
    cur = conn.cursor()                
    cur.execute("SELECT * FROM TEST;")
    machine_data = cur.fetchall()
    conn.commit() 
    cur.close()
    conn.close()
    return machine_data

def main ():
    return testQuery()