from flask import (Flask, render_template)
from generateCertificate import *

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

if __name__ == '__main__':
   app.run()


