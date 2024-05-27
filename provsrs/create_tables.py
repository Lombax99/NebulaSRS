import psycopg2
from config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE MACCHINA(
			id SERIAL PRIMARY KEY,
            descrizione VARCHAR(255),
			CERT BYTEA NOT NULL, 
			CONF BYTEA NOT NULL
		    );
        """,
        """ 
        CREATE TABLE UTENTE (
		    id SERIAL PRIMARY KEY,
		    username VARCHAR(255) UNIQUE NOT NULL
		    );
        """,
        """
        CREATE TABLE USA (
            id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL REFERENCES UTENTE(id),
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id),
            UNIQUE (utente_id, macchina_id)
            );
        """)
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statementS
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    
if __name__ == '__main__':
    create_tables()