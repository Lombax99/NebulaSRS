import psycopg2
import os
from config import load_config

def download(path, name, data):
     with open(path, 'wb') as f:
        f.write(data)
        f.close()
        print(f"{name} downloaded successfully.")
     
def download_files():
    query = "SELECT * FROM MACCHINA;"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Execute the query
                cur.execute(query)

                # Fetch data using fetchall() or iterate with fetchone()
                machine_data = cur.fetchall()  # Fetch all rows at once
                for row in machine_data:
                    id_macchina = row[0]
                    descrizione = row[1] # Descrizione
                    oid_cert = row[2] # cert
                    oid_conf = row[3] # conf

                    #String for files names
                    confname = str(id_macchina)+"_conf.yaml"
                    certname = str(id_macchina)+"_cert.crt"
                    # Controlla
                    # Scarica il cert, se non esiste già
                    pathcrt = os.path.join("src", certname)
                    pathconf = os.path.join("src", confname)
                    if not (os.path.exists(pathcrt)):
                        download(pathcrt, certname, oid_cert)
                    else: 
                        print(f"{certname} already exists")
                    # Scarica il conf, se non esiste già
                    if not (os.path.exists(pathconf)):
                        download(pathconf, confname, oid_conf)
                    else:
                        print(f"{confname} file already exists")

    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        conn.close()

if __name__ == '__main__':
    download_files()
