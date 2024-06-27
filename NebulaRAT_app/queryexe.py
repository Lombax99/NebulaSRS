
from settings import postgresql as settings
import psycopg2

def execute_query():
    command = "SELECT * FROM TEST;"
    try:
       with psycopg2.connect(user=settings['pguser'], password=settings['pgpassword'], host=settings['pghost'], port=settings['pgport'], database=settings['pgdb']) as conn:
            with conn.cursor() as cur:
                # execute the statement
                cur.execute(command)
                machine_data = cur.fetchall()
    except (psycopg2.DatabaseError, Exception) as error:
        return str(error)
    return machine_data