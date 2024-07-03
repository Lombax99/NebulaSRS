#from generateCertificate import *
from settings import postgresql as settings
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, flash
from queryexe import execute_query
from queries import *
from models import secret
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
#import yaml
#import os
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

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

class Usa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    macchina_id = db.Column(db.Integer)
    utente_id = db.Column(db.Integer)

    def __init__(self, macchina_id=None, utente_id=None):
        self.macchina_id = macchina_id
        self.utente_id = utente_id

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
    # if user is logged, we go to dashboard
    if current_user.is_authenticated:
        if current_user.username == 'administration@admin.nebularat.com':
            return redirect(url_for('dashboard_admin', username=current_user.nome))
        else:
            return redirect(url_for('dashboard', username=current_user.nome))
    form = LoginForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(bytes(user.password), form.password.data):
                login_user(user)
                if form.username.data == 'administration@admin.nebularat.com':
                    return redirect(url_for('dashboard_admin', username=user.nome))
                else:
                    return redirect(url_for('dashboard', username=user.nome))
    return render_template('login.html', form=form)



@app.route('/dashboard/<username>')
@login_required
def dashboard(username):
    # Mostra solo le macchine a cui ha il permesso di accedere
    macchine = db.session.execute(text(build_query("utente", current_user.username)))
    return render_template('dashboard.html', macchine=macchine, username=current_user.nome)

@app.route('/dashboard_admin/<username>')
@login_required
def dashboard_admin(username):
    # Mostra tutte le macchine nel sistema
    macchine = db.session.execute(text(tutte))
    return render_template('dashboard_admin.html', macchine=macchine, username=current_user.nome)

@app.route('/adduser', methods=['GET','POST'])
def adduser():
    # Crea oggetto per il form
    formReg = RegisterForm()
    # Retreiving dei valori 
    if formReg.validate_on_submit():
        # password hashata
        hashed_password = bcrypt.generate_password_hash(formReg.password.data)
        # nome
        nome = formReg.name.data
        # cognome
        cognome = formReg.surname.data
        # email
        username = formReg.username.data
        # Crea un nuovo utente
        new_user = Utente(nome=nome, cognome=cognome, username=username, password=hashed_password)
        # lo aggiunge al db
        db.session.add(new_user)
        db.session.commit()
        # reindirizza verso la dashboard dell'admin, visto che è
        # l'unico che può aggiungere nuovi utenti
        return redirect(url_for('dashboard_admin', username=current_user.nome))

    return render_template('signup.html', form=formReg)


@app.route('/404')
def errorPage():
    print('Request for index page received')
    return render_template('404.html')

######################## TEST END #################################
###################################################################


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
######################## TEST END #################################
###################################################################

@app.route('/firerules', methods=['POST'])
def printFwRules():
    # Riceve il valore dell'IP della macchina da cercare
    ip_addr = str(request.form['bottone'])
    # Ricava le rules dall'IP della macchina
    rules = db.session.execute(text(build_query("firewall", ip_addr)))

    # Differenziazione tra admin e basic user
    if current_user.username == 'administration@admin.nebularat.com':
        return render_template('firerules_admin.html', rules=rules, username=current_user.nome)
    else:
        return render_template('firerules.html', rules=rules, username=current_user.nome)
        
@app.route('/list')
def list():
    # Retrieving degli utenti escluso l'admin
    users = db.session.execute(text(utenti))
    return render_template('list_users.html', users=users, username=current_user.nome)

@app.route('/assign', methods=['POST'])
def assig():
    # Riceve il nome e il cognome dell'utente
    email = str(request.form['user'])
    nomeC = db.session.execute(text(build_query("whois", email))).first()
    # Ricava le lista delle macchine a cui l'utente già accede
    accede = db.session.execute(text(build_query("acc", email))).all()
    # Ricava tutte le macchine
    macchine  = db.session.execute(text(mac))
    return render_template('assign.html', email=email, nomeC=nomeC, accede=accede, macchine=macchine, username=current_user.nome)

@app.route('/assignment/<idut>', methods=['GET','POST'])
def assignment(idut):
    checked_machines = request.form.getlist('macc')
    # For each machine id retreived, adds the machine to the user
    for idmac in checked_machines:
        new_usa = Usa(utente_id = idut, macchina_id=idmac)
        db.session.add(new_usa)
        db.session.commit()
    return redirect(url_for('list'))


@app.route('/revoke', methods=['POST'])
def revoke():
    # Riceve il nome e il cognome dell'utente
    email = str(request.form['user'])
    nomeC = db.session.execute(text(build_query("whois", email))).first()
    # Ricava le lista delle macchine a cui l'utente già accede
    accede = db.session.execute(text(build_query("revocation", email))).all()
    return render_template('revoke.html', email=email, nomeC=nomeC, accede=accede, username=current_user.nome)

@app.route('/revokation/<idut>', methods=['GET','POST'])
def revokation(idut):
    checked_machines = request.form.getlist('macc')
    # For each machine id retreived, revokes the machine to the user
    for idmac in checked_machines:
        usa = db.session.get(Usa, idmac)
        db.session.delete(usa)
        db.session.commit()
    return redirect(url_for('list'))

@app.route('/logout')
def logout():
    logout_user()
    flash("Logout effettuato!")
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)

