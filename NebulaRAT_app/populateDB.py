import psycopg2
from settings import postgresql as settings
import time

test_data = {
    "TEST": [
        (0, 'CULO'),
        (1, 'PALLE'),
        (2, "altre palle"),
        (3, "più palle"),
        (4, "ancora più palle")
    ],
    "MACCHINA": [
        (0, 'macchina1', 0, 0),
        (1, 'macchina2', 1, 1)
    ],
    "CONF": [
        (0, '192.168.1.1', 'timeout_tcp', 'timeout_udp', 'timeout_def'),
        (1, '192.168.1.2', 'timeout_tcp', 'timeout_udp', 'timeout_def')
    ],
    "USA":[
        (0, 0, 0),
        (1, 1, 1)
    ],
    "UTENTE": [
        (0, 'luca', 'L', 'xD_darkangelcraft_xD', 'dipartimento dei migliori'),
        (1, 'marco', 'M', 'xX_MagicMikeLove_Xx', 'human resources wink wink'),
        (2, 'stefano', 'S', 'xX_St3f4n0_Xx', 'dipartimento degli spritz')
    ],
    "CERT": [
        (0, 'hahahahnonleggeretemaicosahoscrittoinquestocodicesupersegretissimo'),
        (1, 'enemmenoinquestocodicecisonoanchepasswordveresupersegretissime')
    ],
    "REGOLA": [
        (0, 'in', 37, 'PortStort', 'Prot1', 'Host_aggio', 'ca_name', 'group', 'cidr'),
        (1, 'out', 73, 'PortDritt', 'Prot2', 'Host_ello', 'ca_name', 'group', 'cidr')
    ]
}

def insert_in_table(conn, table_name, data):
    try:
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()
        
        # Define the SQL query to insert data
        if table_name == "MACCHINA":
            query = f"INSERT INTO {table_name} (id, descrizione, cert, conf) VALUES (%s, %s, %s, %s)"
        elif table_name == "UTENTE":
            query = f"INSERT INTO {table_name} (id, nome, cognome, username, password) VALUES (%s, %s, %s, %s, %s)"
        elif table_name == "USA":
            query = f"INSERT INTO {table_name} (id, utente_id, macchina_id) VALUES (%s, %s, %s)"
        elif table_name == "CERT":
            query = f"INSERT INTO {table_name} (id, descrizione) VALUES (%s, %s)"
        elif table_name == "REGOLA":
            query = f"INSERT INTO {table_name} (id, inout, conf_id, port, proto, host, ca_name, gruppi, cidr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        elif table_name == "TEST":
            query = f"INSERT INTO {table_name} (id, description) VALUES (%s, %s)"
        elif table_name == "CONF":
            query = f"INSERT INTO {table_name} (id, ip_addr, tcp_timeout, udp_timeout, def_timeout) VALUES (%s, %s, %s, %s, %s)"
        else: 
            print("Table not found")
            return "Table not found"
        
        # Execute the SQL query for each data row
        for row in data:
            cur.execute(query, row)
        
        # Commit the changes to the database
        conn.commit()
        
        # Close the cursor
        cur.close()
        
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error while filling table:", error)
        return str(error)

def create_test_tables(conn):
    #this tables do not have the references and are just to test if the queries work correctly
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE MACCHINA(
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(255),
            cert  INTEGER NOT NULL,
            conf INTEGER NOT NULL
        );
        """,
        """ 
        CREATE TABLE UTENTE (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cognome VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255)
		);
        """,
        """
        CREATE TABLE USA (
        	id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL,
            macchina_id INTEGER NOT NULL,
            UNIQUE (utente_id, macchina_id)
        );
        """,
        """
        CREATE TABLE CERT (
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(512) NOT NULL
            );
        """,
        """
        CREATE TABLE REGOLA (
            id SERIAL NOT NULL,
            inout VARCHAR(10) NOT NULL,
            conf_id INTEGER NOT NULL,
            port VARCHAR(10),
            proto VARCHAR(10),
            host VARCHAR(255),
            ca_name VARCHAR(255),
            gruppi VARCHAR(500),
            cidr VARCHAR(20)
        );
        """,
        """
        CREATE TABLE TEST (
            id SERIAL PRIMARY KEY,
            description VARCHAR(255) NOT NULL
            );
        """,
        """
        CREATE TABLE CONF (
        	id SERIAL PRIMARY KEY,
            ip_addr VARCHAR(20) UNIQUE NOT NULL,
            tcp_timeout VARCHAR(255),
            udp_timeout VARCHAR(255),
            def_timeout VARCHAR(255)
        );
        """
    )
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def upload_test_data(conn):

    # Commit the changes to the database
    conn.commit()
    try:
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Drop all existing tables
        cur.execute("DROP TABLE IF EXISTS MACCHINA, UTENTE, USA, CERT, REGOLA, TEST, CONF")
        create_test_tables(conn)

        for table_name, data in test_data.items():
            
            # Truncate the table to remove all data
            cur.execute(f"TRUNCATE TABLE {table_name}")
            
            # Insert data into the table
            insert_in_table(conn, table_name, data)

            # Fetch all the data from the current table
            cur.execute(f"SELECT * FROM {table_name}")
            rows = cur.fetchall()

            # Print the data
            for row in rows:
                print(row)

            # Add a sleep of 2 seconds
            time.sleep(2)

        # Close the cursor and connection
        cur.close()
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error while filling table:", error)
        return str(error)


def upload_machines(conn, filepath):
    try:
        data = []
        insert_in_table(conn, "MACCHINA", data)        
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error while filling table:", error)
        return str(error)    

def main():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            user=settings['pguser'],
            password=settings['pgpassword'],
            host=settings['pghost'],
            port=settings['pgport'],
            database=settings['pgdb']
        )
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error while connecting to PostgreSQL", error)
        return str(error)
    
    upload_test_data(conn)
    #upload_machines(conn, "file.json")

    '''# Define your data to be inserted
    data = [
        (0, 'CULO'),
        (1, 'PALLE'),
        (2, "altre palle"),
        (3, "più palle"),
        (4, "ancora più palle")
    ]

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()
    # Truncate the TEST table to remove all data
    cur.execute("TRUNCATE TABLE TEST")

    insert_in_table(conn, "TEST", data)

    # Fetch all the data from the TEST table
    cur.execute("SELECT * FROM TEST")
    rows = cur.fetchall()

    # Print the data
    for row in rows:
        print(row)

    # Close the cursor and connection
    cur.close()'''

    # Close the connection
    conn.close()




if __name__ == "__main__":
    main()