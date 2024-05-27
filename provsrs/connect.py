#Questo script utilizza il modulo config.py per leggere la configurazione del database e connettersi a PostgreSQL
import psycopg2
from config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    print('Connecting to the PostgreSQL database server...')
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)