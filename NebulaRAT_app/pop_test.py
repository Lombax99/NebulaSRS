import psycopg2
from settings import postgresql as settings
import time
import json
from app import bcrypt

test_data = {
    "UTENTE": [
        ('Luca', 'Lombardi', 'luca@nebularat.com', bcrypt.generate_password_hash('luca')),
        ('Marco', 'Marchi', 'marco@nebularat.com', bcrypt.generate_password_hash('marco')),
        ('Stefano', 'Paparella', 'stefano@nebularat.com', bcrypt.generate_password_hash('stefano')),
        ('admin', 'admin', 'administration@admin.nebularat.com', bcrypt.generate_password_hash('admin')),
        ('Antonio', 'Monelli', 'antonio@nebularat.com', bcrypt.generate_password_hash('antonio')),
        ('Pasquale', 'Basta', 'pasquale@nebularat.com', bcrypt.generate_password_hash('pasquale')),
        ('Test', 'RealUser', 'nebulasrs@gmail.com', bcrypt.generate_password_hash('test'))
    ],
    "CERT": [
        (1,"""-----BEGIN NEBULA CERTIFICATE-----
            CmQKBmFkbWluMhIK5MihhQyA/v//DyiU3bezBjCUvrmzBjognides04bE5q5oLFu
            b9DFRyw5F6ybQ06GSmKcZEVM1W5KIKEMXGhjCUfmR6zpDw5OE13aJqAZ5UBh6rbM
            2PJe9OHuEkAuv+YZGe+AXTmS4B37npr1qURxWhwXJBkzth08Y5csRse8whAhNSCR
            m/kjOt3u8F09VOszUJJsbNr/gHP8w0wC
            -----END NEBULA CERTIFICATE-----"""),
        (2,"""-----BEGIN NEBULA CERTIFICATE-----
            CnkKB2xhcHRvcDESCovIoYUMgP7//w8iCExhcHRvcFNEIghTZXJ2ZXJTRCiqye2t
            BjCQsPK8Bjogb5TKN0XccSK9B3hcUIywSUpVvbmsH8/ZkuHrOZNeki9KIKEMXGhj
            CUfmR6zpDw5OE13aJqAZ5UBh6rbM2PJe9OHuEkBwSdgyl6y6/2yYGlFDRfzApCKu
            vVps8qfR/QukM4827MJ77g/ACe/cturaT4BPfreS0IuQ2dOyMUzkkPgwKpcK
            -----END NEBULA CERTIFICATE-----"""),
        (3, """-----BEGIN NEBULA CERTIFICATE-----
            CjwKCk15b3JnLCBJbmMokcntrQYwkbDyvAY6IFxDdM4weRdch/weZFibIWzp3GAR
            GC2k+wF0UuzEFYkIQAESQFM9qMuKKRXKPmmxWdcEt2xT++oShUZlURDPLa0b9Hk1
            jzPw370QRwAggKolbxCxhhDw6GoF6AZRxVdbKgUYHAA=
            -----END NEBULA CERTIFICATE-----""")
    ],
    "MACCHINA": [
        ('macchina1', '192.168.1.1', 1),
        ('macchina2', '192.168.1.2', 2),
        ('macchina3', '192.168.1.3', 3)
    ],
    "REGOLA": [
        ('in', 1, 'PortStort', 'Prot1', 'Host_aggio', 'Myorg, Inc', 'group', '192.168.100.111/32'),
        ('out', 1, 'PortDritt', 'Prot2', 'Host_ello', 'ca_name', 'group', '192.168.100.112/32'),
        ('in', 2, 'PortStort2', 'Prot1_2', 'Host_enta', 'Myorg, Inc', 'group2', '192.168.100.113/32'),
        ('out', 2, 'PortDritt2', 'Prot2_2', 'Host_inato', 'ca_name2', 'group2', '192.168.100.121/32'),
        ('in', 3, 'PortStort3', 'Prot3_1', 'Host_aggio', 'Myorg, Inc', 'rickrolls', '192.168.100.114/32'),
        ('out', 3, 'PortDritt3', 'Never', 'Host_inato', 'ca_name3', 'rickrolls', '192.168.100.122/32')
    ],
    "USA":[
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 1)
    ],
    "TEST": [
        (1,'CULO'),
        (2,'PALLE'),
        (3,"altre palle"),
        (4,"più palle"),
        (5,"ancora più palle")
    ]
}

def insert_in_table(conn, table_name, data):
    try:
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()
        
        # Define the SQL query to insert data
        if table_name == "MACCHINA":
            query = f"INSERT INTO {table_name} (descrizione, ip_addr, cert) VALUES (%s, %s, %s)"
        elif table_name == "UTENTE":
            query = f"INSERT INTO {table_name} (nome, cognome, username, password) VALUES (%s, %s, %s, %s)"
        elif table_name == "USA":
            query = f"INSERT INTO {table_name} (utente_id, macchina_id) VALUES (%s, %s)"
        elif table_name == "CERT":
            query = f"INSERT INTO {table_name} (id, descrizione) VALUES (%s, %s)"
        elif table_name == "REGOLA":
            query = f"INSERT INTO {table_name} (inout, macchina_id, port, proto, host, ca_name, gruppi, cidr) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        elif table_name == "TEST":
            query = f"INSERT INTO {table_name} (id, description) VALUES (%s, %s)"
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
        CREATE TABLE UTENTE (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cognome VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password BYTEA NOT NULL,
            auth INTEGER DEFAULT 0,
            admin INTEGER DEFAULT 0
		);
        """,
        """
        CREATE TABLE CERT (
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(511) NOT NULL
        );
        """,
        """
        CREATE TABLE MACCHINA (
            id SERIAL PRIMARY KEY,
            descrizione VARCHAR(255),
            ip_addr VARCHAR(20) UNIQUE NOT NULL,
            cert  INTEGER NOT NULL REFERENCES CERT(id)
        );
        """,
        """
        CREATE TABLE REGOLA(
			id SERIAL NOT NULL,
			inout varchar(10) NOT NULL,
			macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id) ON DELETE CASCADE,
			port VARCHAR(10),
			proto VARCHAR(10),
			host VARCHAR(255),
			ca_name VARCHAR(255),
			gruppi VARCHAR(500),
			cidr VARCHAR(20)
        );
        """,
        """
        CREATE TABLE USA (
        	id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL REFERENCES UTENTE(id) ON DELETE CASCADE,
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id) ON DELETE CASCADE,
            UNIQUE (utente_id, macchina_id)
        );
        """,
        """
        CREATE TABLE TEST (
            id SERIAL PRIMARY KEY,
            description VARCHAR(255) NOT NULL
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
        cur.execute("DROP TABLE IF EXISTS USA, REGOLA, MACCHINA, CONF, CERT, UTENTE, TEST")
        create_test_tables(conn)

        for table_name, data in test_data.items():
            
            # Truncate the table to remove all data
            #cur.execute(f"TRUNCATE TABLE {table_name}")
            
            # Insert data into the table
            insert_in_table(conn, table_name, data)

            # Sets the admin flag
            cur.execute("UPDATE UTENTE SET admin = 1 WHERE username = 'administration@admin.nebularat.com'")

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
        # Read the data from networkConfig.json
        with open("nebulaFiles/networkConfig.json") as file:
            data = json.load(file)

        # Extract the required values from the data
        values = []
        for machine in data:
            values.append((machine["descrizione"], machine["cert"], machine["config"]))
        
        # Insert the values into the MACCHINA table
        #insert_in_table(conn, "MACCHINA", values)

        # upload of certificate values

        # upload of config data in CONF table

        # upload of single rules in REGOLA table


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

    # Close the connection
    conn.close()




if __name__ == "__main__":
    main()