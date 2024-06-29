#from generateCertificate import *
from settings import postgresql as settings
from flask import Flask, render_template, request, jsonify
from queryexe import execute_query
from queryexe import execute_query
from queries import *
#import yaml
#import os
app = Flask(__name__)

@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/login')
def login():
    print('Request for index page received')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = "xX_MagicMikeLove_Xx"  #da modificare quando si crea la sessione di login
    query = build_query("macchine", username)
    macchine = execute_query(query)
    print('Request for dashboard page received')
    return render_template('dashboard.html', macchine=macchine)

@app.route('/signup')
def signup():
    print('Request for index page received')
    return render_template('signup.html')

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
    return execute_query(test)

@app.route('/mostra-ip-descr')
def mostraIpDescr():
    utente = "xX_MagicMikeLove_Xx"
    query = build_query("utente", utente)
    return execute_query(query)

@app.route('/firerules', methods=['POST'])
def printFwRules():
    ip_addr = str(request.form['bottone'])
    query = build_query("firewall", ip_addr)
    rules = execute_query(query)
    print('Request for dashboard page received')
    print(ip_addr)
    return render_template('firerules.html', rules=rules)


if __name__ == '__main__':
   app.run(debug=True)

