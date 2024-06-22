#import psycopg2


def test():
    """cnxn = pyodbc.connect(
        'DRIVER=' + DRIVER + ';PORT=5432;SERVER=' + SERVER +
        ';PORT=5432;DATABASE=' + DATABASE + ';UID=' + USERNAME +
        ';PWD=' + PASSWORD)
    cursor = cnxn.cursor()
    selectsql = "SELECT * FROM TEST;" # SALES is an example table name
    cursor.execute(selectsql)
    rows = cursor.fetchall()

    cnxn.commit()
    cursor.close()
    cnxn.close()

    return rows"""