from flask import (Flask, render_template)
from generateCertificate import *

app = Flask(__name__)

@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

if __name__ == '__main__':
   app.run()