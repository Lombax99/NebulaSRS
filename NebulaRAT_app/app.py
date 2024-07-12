from generateCertificate import *
import pyotp
import zipfile
import queries
from settings import postgresql as psql
from settings import secret, outputDir
from flask import Flask, redirect, render_template, request, jsonify, session, url_for, flash
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import text
from flask import send_file
from tfaLib import *
from defences import is_pathTraversal
# Database URI
db_uri = f"postgresql+psycopg2://{psql['pguser']}:{psql['pgpassword']}@{psql['pghost']}:{psql['pgport']}/{psql['pgdb']}"
# App configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SECRET_KEY'] = secret
# Istantiates DB
db = SQLAlchemy(app)
# Bcrypt object
bcrypt = Bcrypt(app)
# Generate a secret key
secret_key = pyotp.random_base32()
    
# Create a TOTP object
totp = pyotp.TOTP(secret_key)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Utente.query.get(int(user_id))

#############################################################################################################################################
############################################################### CLASSES START ###############################################################


# User class
class Utente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(255), nullable=False)
    cognome = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    auth = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Integer, nullable=False)

# Class that links machines and users
class Usa(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    macchina_id = db.Column(db.Integer)
    utente_id = db.Column(db.Integer)

    def __init__(self, macchina_id=None, utente_id=None):
        self.macchina_id = macchina_id
        self.utente_id = utente_id

# Form for registering a new user
class RegisterForm(FlaskForm):
    
    name = StringField(validators=[InputRequired()], render_kw={"class":"form-control","placeholder": "Mario"})
    
    surname = StringField(validators=[InputRequired()], render_kw={"class":"form-control","placeholder": "Rossi"})
    
    username = StringField(validators=[InputRequired()], render_kw={"type":"email", "class":"form-control","aria-describedby":"emailHelp", "placeholder":"mariorossi12@nebularat.com"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Password"})

    submit = SubmitField('Add user', render_kw={"type":"submit", "class":"btn btn-primary py-3 mb-4"})

    def validate_username(self, username):
        existing_user_username = Utente.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Username already exists. Please try a different username.')

# Form for login       
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"type":"email", "class":"form-control","aria-describedby":"emailHelp", "placeholder":"mariorossi12@nebularat.com"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Password"})

    submit = SubmitField('Login', render_kw={"type":"submit", "class":"btn btn-primary py-3 w-100 mb-4"})

# Form for changing the password
class ChangePw(FlaskForm):
    oldpassword = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Old password"})

    password = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "New password"})

    repeat = PasswordField(validators=[InputRequired()], render_kw={"type":"password", "class":"form-control", "placeholder": "Repeat password"})

    submit = SubmitField('Change Password', render_kw={"type":"submit", "class":"btn btn-primary py-3 mb-4"})

# Form for the 2FA
class FactorAuth(FlaskForm):
    code = StringField(validators=[InputRequired()], render_kw={"type":"text", "class":"form-control", "placeholder":"2FA code here"})

    submit = SubmitField('Submit', render_kw={"type":"submit", "class":"btn btn-primary py-3 w-100 mb-4"})

#############################################################################################################################################
################################################################ CLASSES END ################################################################ 

@app.route('/')
def root():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    # if user is logged, we go to dashboard
    msg=""
    if current_user.is_authenticated:
        if session["admin"] == 1:
            return redirect(url_for('dashboard_admin', username=current_user.nome))
        else:
            return redirect(url_for('dashboard', username=current_user.nome))
    form = LoginForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(bytes(user.password), form.password.data):
                session["username"] = user.username
                # Checks if the user has the 2fa activated
                if user.auth == 1:
                    send_2fa(totp, session["username"])
                    return redirect(url_for('user_authentication'))
                else:
                    # Directly logs in
                    session["id"] = user.id
                    session["nome"] = user.nome
                    session["cognome"] = user.cognome
                    session["auth"] = user.auth
                    session["admin"] = user.admin
                    # Logs the user in
                    login_user(user)
                    # Redirects to the dashboard
                    if session["admin"] == 1:
                        return redirect(url_for('dashboard_admin'))
                    else:
                        return redirect(url_for('dashboard'))
            else:
                msg="Wrong password! Try again!"
        else:
            msg="User doesn't exist!"
    return render_template('login.html', form=form, msg=msg)

@app.route('/user_authentication', methods=['GET','POST'])
def user_authentication():
    msg = "" 
    # Creates the form object
    form = FactorAuth()
    if form.validate_on_submit():
        # Checks if the code is correct
        if check_2fa(totp, form.code.data):
            # If the code is correct, the user is logged in
            user = Utente.query.filter_by(username=session["username"]).first()
            session["id"] = user.id
            session["nome"] = user.nome
            session["cognome"] = user.cognome
            session["auth"] = user.auth
            session["admin"] = user.admin
            # Logs the user in
            login_user(user)
            # Redirects to the dashboard
            if session["admin"] == 1:
                return redirect(url_for('dashboard_admin'))
            else:
                return redirect(url_for('dashboard'))
        else:
            # If the code is incorrect, the user is redirected to the 2fa page again
            send_2fa(totp, session["username"])
            msg="Invalid 2FA code. Please try again."
    return render_template('user_authentication.html', form=form, msg=msg)
            

@app.route('/change_password', methods=['GET','POST'])
def change_password():
    msg=""
    form = ChangePw()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=session["username"]).first()
        # Controls if the old password is correct (he is who he says to be)
        if bcrypt.check_password_hash(bytes(user.password), form.oldpassword.data):
            # Checks if the user hasn't used the old password
            if not bcrypt.check_password_hash(bytes(user.password), form.password.data):
                # Checks if the new password and its replica are equals
                if form.password.data != form.repeat.data:
                    msg="Passwords don't match"
                else:
                    # Hashes the new password and updates the db
                    hashed_password = bcrypt.generate_password_hash(form.password.data)
                    user.password = hashed_password
                    db.session.commit()
                    # Chooses where to go after the password change
                    if session["admin"] == 1:
                        return redirect(url_for('dashboard_admin'))
                    else:
                        return redirect(url_for('dashboard'))
            else:
                msg="You can't use the old password"
        else:
            msg="Wrong password!"
    return render_template('change_password.html', form=form, admin=session["admin"], msg=msg)

@app.route('/dashboard')
@login_required
def dashboard():
    # Username to show in the dashboard
    username = session["nome"] + " " + session["cognome"]
    # Show only the machines that the user has permission to access
    macchine = db.session.execute(text(queries.sel_macchine % session["username"]))
    return render_template('dashboard.html', macchine=macchine, username=username)

@app.route('/dashboard_admin')
@login_required
def dashboard_admin():
    # Shows all the machines
    macchine = db.session.execute(text(queries.tutte))
    return render_template('dashboard_admin.html', macchine=macchine, username=session["nome"])

@app.route('/adduser', methods=['GET','POST'])
@login_required
def adduser():
    msg=""
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
        user = Utente.query.filter_by(username=username).first()
        if user:
            msg="User already exists!"
        else:
            # A2F is disativated by default
            a2f = 0
            # It's not an admin
            admin = 0
            # Creates new user
            new_user = Utente(nome=nome, cognome=cognome, username=username, password=hashed_password, auth=a2f, admin=admin)
            # adds it to the db
            db.session.add(new_user)
            db.session.commit()
            # redirect to the admin dashboard, as only the admin can add new users
            return redirect(url_for('dashboard_admin'))
    return render_template('signup.html', form=formReg, username=session["username"], msg=msg)

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
    return "hello world"

@app.route('/mostra-ip-descr')
def mostraIpDescr():
    return "hello world"
######################## TEST END #################################
###################################################################

@app.route('/firerules', methods=['POST'])
@login_required
def printFwRules():
    # Riceve il valore dell'IP della macchina da cercare
    ip_addr = str(request.form['bottone'])
    # Ricava le rules dall'IP della macchina
    rules = db.session.execute(text(queries.firewall), {'ip_addr': ip_addr}).all()

    # Differenziazione tra admin e basic user
    if current_user.admin == 1:
        return render_template('firerules_admin.html', rules=rules, username=current_user.nome)
    else:
        return render_template('firerules.html', rules=rules, username=current_user.nome)
        
@app.route('/list')
@login_required
def list():
    # Retrieving degli utenti escluso l'admin
    users = db.session.execute(text(queries.utenti % session["admin"]))
    return render_template('list_users.html', users=users, username=current_user.nome)

@app.route('/assign', methods=['POST'])
def assign():
    # Riceve il nome e il cognome dell'utente
    email = str(request.form['user'])
    user = Utente.query.filter_by(username=email).first()
    # Ricava le lista delle macchine a cui l'utente già accede
    accede = db.session.execute(text(queries.acc), {'email': email}).all()
    # Retrieves all machines
    macchine  = db.session.execute(text(queries.mac))
    return render_template('assign.html', email=email, id=user.id, nomeC=user.nome, cognomeC=user.cognome,  accede=accede, macchine=macchine, username=current_user.nome)

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
    # Receives the name and surname of the user
    email = str(request.form['user'])
    user = Utente.query.filter_by(username=email).first()
    # Retrieves the list of machines that the user already has access to
    accede = db.session.execute(text(queries.revocation % email)).all()
    return render_template('revoke.html', email=email, id=user.id, nomeC=user.nome, cognomeC=user.cognome, accede=accede, username=current_user.nome)

@app.route('/revokation/<idut>', methods=['GET','POST'])
def revokation(idut):
    checked_machines = request.form.getlist('macc')
    # For each machine id retreived, revokes the machine to the user
    for idmac in checked_machines:
        usa = db.session.get(Usa, idmac)
        db.session.delete(usa)
        db.session.commit()
    return redirect(url_for('list'))

def download(path):
    return send_file(path, as_attachment=True)  

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    # The certificate generation script expects a CIDR and a duration
    cidr = str(request.form['genbtn'])
    duration = str(request.form['dur'])
    print(f"cidr: {cidr}")
    print(f"duration: {duration}")
    # Generates the certificate for the machine
    pathcrt, pathkey, outputDir = generate_Certificate(session["nome"], cidr, duration)
    # Creates a zip file with crt and key 
    zip_path = os.path.join(outputDir, session["nome"] + ".zip")
    # Path traversal check
    if is_pathTraversal(os.path.basename(pathcrt)) or is_pathTraversal(os.path.basename(pathkey)) or is_pathTraversal(os.path.basename(zip_path)):
        return render_template('404.html') #Bad user!
    else:
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            zip_file.write(pathcrt, os.path.basename(pathcrt))
            zip_file.write(pathkey, os.path.basename(pathkey))
        # Removes crt and key files
        os.remove(pathcrt)
        os.remove(pathkey)
        # Downloads zip file
        return send_file(zip_path, as_attachment=True)
    
@app.route('/profile')
def profile():
    return render_template("profile.html", nome=session["nome"], cognome=session["cognome"], username=session["username"], auth=session["auth"], admin=session["admin"])

@app.route('/activate', methods=['GET','POST'])
def activate():
    switch = request.form.get("authSwitch")
    user = Utente.query.filter_by(username=session["username"]).first()
    if switch == "1":
        user.auth = 1
    else:
        user.auth = 0
    db.session.commit()
    session["auth"]=user.auth
    return redirect(url_for('profile'))

@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    email = str(request.form['utente'])
    # Deletes the user from the db
    user = Utente.query.filter_by(username=email).first()
    db.session.delete(user)
    db.session.commit()
    # Prints a message of correctly deleted user on the page
    flash("User correctly deleted!", "info")
    return redirect(url_for('list'))

@app.route('/errorPage')
def errorPage():
    return render_template('404.html')

@app.route('/logout')
@login_required
def logout():
    session.pop("id", None)
    session.pop("nome", None)
    session.pop("cognome", None)
    session.pop("username", None)
    session.pop("auth", None)
    session.pop("admin", None)
    logout_user()
    return redirect('/')

if __name__ == '__main__':
   app.run(debug=True)

