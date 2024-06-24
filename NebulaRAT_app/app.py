#from generateCertificate import *
from settings import postgresql as settings
from flask import Flask, render_template, request, jsonify
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import postgresql as settings


db_uri = f"postgresql+psycopg2://{settings['pguser']}:{settings['pgpassword']}@{settings['pghost']}:{settings['pgport']}/{settings['pgdb']}"
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# initialize the database connection
db.init_app(app)

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    descrizione = db.Column(db.String(255))

    def __init__(self, descrizione=None):
        self.descrizione = descrizione

with app.app_context():
    db.create_all()

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
    #return get_certificate(machineName + ".crt")
    return "ciao"

@app.route('/test-python-function-DB')
def testPythonFunctionDB():
    result = Prova.query.all()
    return result



if __name__ == '__main__':
   app.run(debug=True)


