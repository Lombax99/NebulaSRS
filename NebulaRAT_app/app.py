from generateCertificate import *
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
import os
from sqlalchemy import text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
import shutil
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

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

class ChangePw(FlaskForm):
    oldpassword = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Old password"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "New password"})

    repeat = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Repeat password"})

    submit = SubmitField('Change Password', render_kw={"type":"submit", "class":"btn btn-primary py-3 w-100 mb-4"})



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
                session["id"] = user.id
                session["nome"] = user.nome
                session["cognome"] = user.cognome
                session["username"] = user.username
                login_user(user)
                if form.username.data == 'administration@admin.nebularat.com':
                    return redirect(url_for('dashboard_admin'))
                else:
                    return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/change_password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePw()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=session["username"]).first()
        # Controls if the old password is correct (he is who he says to be)
        if bcrypt.check_password_hash(bytes(user.password), form.oldpassword.data):
            # Checks if the user hasn't used the old password
            if not bcrypt.check_password_hash(bytes(user.password), form.password.data):
                # Checks if the new password and its replica are equals
                if form.password.data != form.repeat.data:
                    flash("Passwords don't match")
                    return redirect(url_for('change_password'))
                else:
                    # Hashes the new password and updates the db
                    hashed_password = bcrypt.generate_password_hash(form.password.data)
                    user.password = hashed_password
                    db.session.commit()
                    # Password changed, the user is not using the old password anymore
                    session["change"] = False
                    # Chooses where to go after the password change
                    if session["username"] == 'administration@admin.nebularat.com':
                        return redirect(url_for('dashboard_admin'))
                    else:
                        return redirect(url_for('dashboard'))
            else:
                flash("You can't use the old password")
                return redirect(url_for('change_password'))
            
    return render_template('change_password.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Username to show in the dashboard
    username = session["nome"] + " " + session["cognome"]
    # Show only the machines that the user has permission to access
    macchine = db.session.execute(text(build_query("utente", session["username"])))
    return render_template('dashboard.html', macchine=macchine, username=username)

@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    # Shows all the machines
    macchine = db.session.execute(text(tutte))
    return render_template('dashboard_admin.html', macchine=macchine, username=session["nome"])

@app.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    # Creates form object
    formReg = RegisterForm()
    # Retreiving dei valori 
    if formReg.validate_on_submit():
        # password 
        hashed_password = bcrypt.generate_password_hash(formReg.password.data)
        # name
        nome = formReg.name.data
        # surname
        cognome = formReg.surname.data
        # email
        username = formReg.username.data
        # Creates new user
        new_user = Utente(nome=nome, cognome=cognome, username=username, password=hashed_password, oldpw=hashed_password)
        # adds it to the db
        db.session.add(new_user)
        db.session.commit()
        # redirect to the admin dashboard, as only the admin can add new users
        return redirect(url_for('dashboard_admin'))

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
@login_required
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
@login_required
def list():
    # Retrieving degli utenti escluso l'admin
    users = db.session.execute(text(utenti))
    return render_template('list_users.html', users=users, username=current_user.nome)

@app.route('/assign', methods=['POST'])
@login_required
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
@login_required
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

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    # Riceve il valore dell'IP della macchina

    # Lo script di generazione del certificato si aspetta un CIDR
    cidr = str(request.form['genbtn'])
    duration = str(request.form['dur'])
    # Genera il certificato per la macchina
    pathcrt, pathkey = generateCertificate(session["nome"], cidr, duration)
    # Ottieni il percorso della cartella Downloads
    # Prompt the user to select a directory
    Tk().withdraw()
    save_path = askdirectory()
    # Copia il file nella cartella selezionata
    shutil.copy(pathcrt, save_path)
    shutil.copy(pathkey, save_path)
    # Rimuove i file temporanei
    os.remove(pathcrt)
    os.remove(pathkey)
    # Controlla se si tratta dell'admin o di un utente base
    if current_user.username == 'administration@admin.nebularat.com':
        return redirect(url_for('dashboard_admin'))
    else:
        return redirect(url_for('dashboard'))

    


@app.route('/logout')
@login_required
def logout():
    session.pop("id", None)
    session.pop("nome", None)
    session.pop("cognome", None)
    session.pop("username", None)
    session.pop("change", None)
    logout_user()
    flash("Logout effettuato!")
    return redirect('/')


if __name__ == '__main__':
   app.run(debug=True)

