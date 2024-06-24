from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from settings import postgresql as settings


def get_engine(user, password, host, port, db):
    url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        return 'Database non esiste'
    
    engine = create_engine(url, pool_size=50, echo=False)

    return engine


def get_engine_from_settings():
    keys = ['pguser', 'pgpassword', 'pghost', 'pgport', 'pgdb']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad config file')
    
    return get_engine(settings['pguser'],
                    settings['pgpassword'],
                    settings['pghost'],
                    settings['pgport'],
                    settings['pgdb'])

def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session

def run_query():
    engine = get_engine_from_settings()
    try:
        with engine.connect() as connection_str:
            return 'Successfully connected to the PostgreSQL database'
    except Exception as ex:
        error = f'Sorry failed to connect: {ex}'
        return error

if __name__ == '__main__':
   run_query()
