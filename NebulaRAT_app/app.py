from flask import Flask, render_template, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from generateCertificate import *
<<<<<<< Updated upstream
import psycopg2 as ps
app = Flask(__name__)

=======
<<<<<<< HEAD
import psycopg2

app = Flask(__name__)

db_connection = psycopg2.connect(
    database="testdb",
    user="Pasquale",
    password="1999",
    host="localhost"
)
=======
import psycopg2 as ps
app = Flask(__name__)

>>>>>>> Stashed changes

def prova():
    query = "SELECT * FROM TEST;"
    cnx = ps.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
    try:
        with cnx as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                machine_data = cur.fetchall()  # Fetch all rows at once
                return machine_data
    except (ps.DatabaseError, Exception) as error:
        print(error)
    finally:
        conn.close()


<<<<<<< Updated upstream
=======
>>>>>>> a79f6a3d03cb70ba931c3403211bd555b90c3420
>>>>>>> Stashed changes

@app.route('/')
def root():
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, descrizione, indirizzoip FROM MACCHINA_Disp")
    macchine = cursor.fetchall()
    cursor.close()
    print('Request for index page received')
    return render_template('index.html',macchine=macchine)

@app.route('/login')
def login():
    print('Request for index page received')
    return render_template('login.html')

@app.route('/signup')
def signup():
    print('Request for index page received')
    return render_template('signup.html')


@app.route('/test')
def testpage():
    print('Request for index page received')
    return render_template('test.html')

@app.route('/test-python-function-JSON')
def testPythonFunction():
    data = {
        'message': 'Hello, world!'
    }
    return jsonify(data)

@app.route('/test-python-function-string')
def testPythonFunctionString():
    return 'Hello, world!'

@app.route('/test-python-function-Certificate')
def testPythonFunctionCertificate():
    return get_certificate(machineName + ".crt")

@app.route('/test-python-function-DB')
def testPythonFunctionDB():
    return prova()




if __name__ == '__main__':
   app.run(debug=True)
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes


