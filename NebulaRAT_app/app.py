from flask import Flask, render_template, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
from generateCertificate import *
app = Flask(__name__)
import psycopg2


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
    #import psycopg2
    
    try:
        with psycopg2.connect(user="sudo", password="sudo", host="nebularat-postgresdb-server.postgres.database.azure.com", port=5432, database="nebularat-postgresServer-db") as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM TEST;")
                machine_data = cur.fetchall() 
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        return 'null'
    finally:
        cur.close()
        conn.close()
        return machine_data
    




if __name__ == '__main__':
   app.run(debug=True)


