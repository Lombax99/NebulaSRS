import psycopg2
from settings import postgresql as settings

def insert_in_table(conn, table_name, data):
    try:
        # Create a cursor object to execute SQL queries
        cur = conn.cursor()
        
        # Define the SQL query to insert data
        query = f"INSERT INTO {table_name} (id, description) VALUES (%s, %s)"
        
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