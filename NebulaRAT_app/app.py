from flask import Flask, render_template, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from generateCertificate import *
import psycopg2
app = Flask(__name__)


def prova():
    query = "SELECT * FROM TEST;"
    cnx = psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db")
    try:
        with cnx as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                machine_data = cur.fetchall()  # Fetch all rows at once
                return machine_data
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        conn.close()



@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/404')
def errorPage():
    print('Request for index page received')
    return render_template('404.html')

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


