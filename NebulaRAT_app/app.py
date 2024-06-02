import os
from flask import (Flask, redirect, render_template, request, send_from_directory, url_for)
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)

@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

if __name__ == '__main__':
   app.run()