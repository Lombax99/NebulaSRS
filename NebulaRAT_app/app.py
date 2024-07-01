#from generateCertificate import *
from settings import postgresql as settings
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, flash
from queryexe import execute_query
from queries import *
from models import session, secret
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
#import yaml
#import os
from sqlalchemy import text

db_uri = f"postgresql+psycopg2://{settings['pguser']}:{settings['pgpassword']}@{settings['pghost']}:{settings['pgport']}/{settings['pgdb']}"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = secret
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))


class Utente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class RegisterForm(FlaskForm):
    
    name = StringField(validators=[InputRequired()], render_kw={"class":"form-control","placeholder": "Mario"})
    
    surname = StringField(validators=[InputRequired()], render_kw={"class":"form-control","placeholder": "Rossi"})
    
    username = StringField(validators=[InputRequired()], render_kw={"type":"email", "class":"form-control","aria-describedby":"emailHelp", "placeholder":"mariorossi12@nebularat.com"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Password"})

    submit = SubmitField('Register', render_kw={"type":"submit", "class":"btn btn-primary py-3 w-100 mb-4"})

    def validate_username(self, username):
        existing_user_username = Utente.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Nome utente già esistente. Riprova con un nome utente diverso.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"type":"email", "class":"form-control","aria-describedby":"emailHelp", "placeholder":"mariorossi12@nebularat.com"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Password"})

    submit = SubmitField('Login', render_kw={"type":"submit", "class":"btn btn-primary py-3 w-100 mb-4"})


@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')



@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(bytes(user.password), form.password.data):
                login_user(user)
                return redirect(url_for('dashboard', username=form.username.data))
    return render_template('login.html', form=form)



@app.route('/dashboard/<username>')
@login_required
def dashboard(username):

    macchine = db.session.execute(text(build_query('utente', username)))
    print('Request for dashboard page received')
    return render_template('dashboard.html', macchine=macchine, username=username)

@app.route('/signup', methods=['GET','POST'])
def signup():
    formReg = RegisterForm()
    if formReg.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(formReg.password.data)
        nome = formReg.name.data
        cognome = formReg.surname.data
        username = formReg.username.data
        new_user = Utente(nome=nome, cognome=cognome, username=username, password=hashed_password)
        print(f"new User: {nome} {cognome} {username} {hashed_password}")
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('signup.html', form=formReg)


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
    rules = db.session.execute(text(build_query('firewall', ip_addr)))
    print('Request for dashboard page received')
    print(ip_addr)
    return render_template('firerules.html', rules=rules)

@app.route('/logout')
def logout():
    logout_user()
    flash("Logout effettuato!")
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)

