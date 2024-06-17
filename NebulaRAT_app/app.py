from flask import Flask, render_template, jsonify
from generateCertificate import *
from test import test
app = Flask(__name__)

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
    data = test()
    return jsonify(data)

@app.route('/test-python-function-String')
def testPythonFunctionString():
    data = test()
    return data

@app.route('/test-python-function-Certificate')
def testPythonFunctionCertificate():
    return get_certificate(machineName + ".crt")

if __name__ == '__main__':
   app.run(debug=True)


